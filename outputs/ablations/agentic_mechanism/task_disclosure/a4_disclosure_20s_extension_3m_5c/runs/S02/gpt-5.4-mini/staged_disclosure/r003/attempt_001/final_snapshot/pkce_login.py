import base64
import hashlib
import os
import secrets
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

import requests

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE")
AUTH0_CALLBACK_HOST = os.environ.get("AUTH0_CALLBACK_HOST", "127.0.0.1")
AUTH0_CALLBACK_PORT = int(os.environ.get("AUTH0_CALLBACK_PORT", "8765"))
AUTH0_SCOPE = os.environ.get("AUTH0_SCOPE", "openid profile email")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def generate_pkce_pair():
    verifier = _b64url(secrets.token_bytes(32))
    challenge = _b64url(hashlib.sha256(verifier.encode()).digest())
    return verifier, challenge


class _CallbackHandler(BaseHTTPRequestHandler):
    code = None
    error = None

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        if "error" in params:
            _CallbackHandler.error = params.get("error_description", [params["error"][0]])[0]
        else:
            _CallbackHandler.code = params.get("code", [None])[0]
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<html><body>You may close this window.</body></html>")

    def log_message(self, format, *args):
        return


def _start_local_server():
    server = HTTPServer((AUTH0_CALLBACK_HOST, AUTH0_CALLBACK_PORT), _CallbackHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def login(timeout_seconds: int = 300):
    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID:
        raise RuntimeError("AUTH0_DOMAIN and AUTH0_CLIENT_ID are required")

    verifier, challenge = generate_pkce_pair()
    redirect_uri = f"http://{AUTH0_CALLBACK_HOST}:{AUTH0_CALLBACK_PORT}/callback"
    server = _start_local_server()
    try:
        auth_url = f"https://{AUTH0_DOMAIN}/authorize?{urlencode({'response_type': 'code', 'client_id': AUTH0_CLIENT_ID, 'redirect_uri': redirect_uri, 'scope': AUTH0_SCOPE, 'code_challenge': challenge, 'code_challenge_method': 'S256', 'state': secrets.token_urlsafe(16), **({'audience': AUTH0_AUDIENCE} if AUTH0_AUDIENCE else {})})}"
        webbrowser.open(auth_url)
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            if _CallbackHandler.error:
                raise RuntimeError(_CallbackHandler.error)
            if _CallbackHandler.code:
                break
            time.sleep(0.2)
        if not _CallbackHandler.code:
            raise TimeoutError("Timed out waiting for authorization code")

        token_resp = requests.post(
            f"https://{AUTH0_DOMAIN}/oauth/token",
            json={
                "grant_type": "authorization_code",
                "client_id": AUTH0_CLIENT_ID,
                "code": _CallbackHandler.code,
                "code_verifier": verifier,
                "redirect_uri": redirect_uri,
            },
            timeout=30,
        )
        token_resp.raise_for_status()
        return token_resp.json()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    print(login())
