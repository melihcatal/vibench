import base64
import hashlib
import secrets
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional

import requests


AUTH0_DOMAIN = "YOUR_TENANT.auth0.com"
AUTH0_CLIENT_ID = "YOUR_PUBLIC_CLIENT_ID"
AUTH0_AUDIENCE = ""
AUTH0_SCOPE = "openid profile email"
AUTH0_REDIRECT_URI = "http://127.0.0.1:8765/callback"
AUTH0_AUTHORIZATION_ENDPOINT = f"https://{AUTH0_DOMAIN}/authorize"
AUTH0_TOKEN_ENDPOINT = f"https://{AUTH0_DOMAIN}/oauth/token"


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def generate_pkce_pair() -> tuple[str, str]:
    verifier = _b64url(secrets.token_bytes(32))
    challenge = _b64url(hashlib.sha256(verifier.encode("ascii")).digest())
    return verifier, challenge


def build_authorization_url(state: str, code_challenge: str) -> str:
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "scope": AUTH0_SCOPE,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    if AUTH0_AUDIENCE:
        params["audience"] = AUTH0_AUDIENCE
    return f"{AUTH0_AUTHORIZATION_ENDPOINT}?{urllib.parse.urlencode(params)}"


class _CallbackHandler(BaseHTTPRequestHandler):
    server_version = "Auth0PKCE/1.0"

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != urllib.parse.urlparse(AUTH0_REDIRECT_URI).path:
            self.send_error(404)
            return
        query = urllib.parse.parse_qs(parsed.query)
        self.server.auth_code = query.get("code", [None])[0]
        self.server.auth_state = query.get("state", [None])[0]
        self.server.auth_error = query.get("error", [None])[0]
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<html><body>You may close this tab.</body></html>")

    def log_message(self, format: str, *args) -> None:
        return


def wait_for_callback(expected_state: str, timeout: int = 300) -> str:
    host = urllib.parse.urlparse(AUTH0_REDIRECT_URI).hostname or "127.0.0.1"
    port = urllib.parse.urlparse(AUTH0_REDIRECT_URI).port or 80
    httpd = HTTPServer((host, port), _CallbackHandler)
    httpd.timeout = timeout
    httpd.auth_code = None
    httpd.auth_state = None
    httpd.auth_error = None
    httpd.handle_request()
    if httpd.auth_error:
        raise RuntimeError(httpd.auth_error)
    if httpd.auth_state != expected_state:
        raise RuntimeError("state mismatch")
    if not httpd.auth_code:
        raise RuntimeError("missing authorization code")
    return httpd.auth_code


def exchange_code_for_tokens(code: str, code_verifier: str) -> dict:
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code": code,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "code_verifier": code_verifier,
    }
    response = requests.post(AUTH0_TOKEN_ENDPOINT, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def pkce_login() -> dict:
    code_verifier, code_challenge = generate_pkce_pair()
    state = _b64url(secrets.token_bytes(16))
    auth_url = build_authorization_url(state, code_challenge)
    webbrowser.open(auth_url)
    code = wait_for_callback(state)
    return exchange_code_for_tokens(code, code_verifier)


if __name__ == "__main__":
    print(pkce_login())
