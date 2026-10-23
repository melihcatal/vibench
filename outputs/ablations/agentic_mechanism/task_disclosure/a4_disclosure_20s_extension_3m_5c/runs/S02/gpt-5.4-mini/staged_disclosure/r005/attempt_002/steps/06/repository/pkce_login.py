import base64
import hashlib
import os
import secrets
import threading
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-tenant.us.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "")
AUTH0_SCOPE = os.getenv("AUTH0_SCOPE", "openid profile email")
REDIRECT_HOST = os.getenv("PKCE_REDIRECT_HOST", "127.0.0.1")
REDIRECT_PORT = int(os.getenv("PKCE_REDIRECT_PORT", "8765"))
REDIRECT_PATH = os.getenv("PKCE_REDIRECT_PATH", "/callback")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def generate_pkce_pair() -> tuple[str, str]:
    verifier = _b64url(secrets.token_bytes(32))
    challenge = _b64url(hashlib.sha256(verifier.encode("ascii")).digest())
    return verifier, challenge


def build_authorization_url(redirect_uri: str, code_challenge: str, state: str) -> str:
    params = {
        "client_id": AUTH0_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": AUTH0_SCOPE,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    if AUTH0_AUDIENCE:
        params["audience"] = AUTH0_AUDIENCE
    return f"https://{AUTH0_DOMAIN}/authorize?{urllib.parse.urlencode(params)}"


def exchange_code_for_tokens(code: str, verifier: str, redirect_uri: str) -> dict:
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code": code,
        "code_verifier": verifier,
        "redirect_uri": redirect_uri,
    }
    response = requests.post(token_url, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


class _CallbackHandler(BaseHTTPRequestHandler):
    auth_result = {"code": None, "state": None, "error": None}
    done = threading.Event()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != REDIRECT_PATH:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return
        params = urllib.parse.parse_qs(parsed.query)
        self.auth_result["code"] = params.get("code", [None])[0]
        self.auth_result["state"] = params.get("state", [None])[0]
        self.auth_result["error"] = params.get("error", [None])[0]
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<html><body>Login complete. You may close this window.</body></html>")
        self.done.set()

    def log_message(self, format, *args):
        return


def pkce_login() -> dict:
    if not AUTH0_CLIENT_ID:
        raise ValueError("AUTH0_CLIENT_ID must be set")
    verifier, challenge = generate_pkce_pair()
    state = secrets.token_urlsafe(24)
    redirect_uri = f"http://{REDIRECT_HOST}:{REDIRECT_PORT}{REDIRECT_PATH}"
    auth_url = build_authorization_url(redirect_uri, challenge, state)
    server = HTTPServer((REDIRECT_HOST, REDIRECT_PORT), _CallbackHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    webbrowser.open(auth_url)
    _CallbackHandler.done.wait(timeout=300)
    server.shutdown()
    result = _CallbackHandler.auth_result
    if result["error"]:
        raise RuntimeError(result["error"])
    if result["state"] != state:
        raise RuntimeError("Invalid state")
    if not result["code"]:
        raise RuntimeError("Missing authorization code")
    return exchange_code_for_tokens(result["code"], verifier, redirect_uri)


if __name__ == "__main__":
    tokens = pkce_login()
    print(tokens)
