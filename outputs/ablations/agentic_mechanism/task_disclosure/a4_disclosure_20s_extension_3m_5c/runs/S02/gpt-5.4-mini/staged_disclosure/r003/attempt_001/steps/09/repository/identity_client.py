import base64
import hashlib
import json
import os
import secrets
import threading
import time
import webbrowser
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlencode, urlparse

import requests


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE")
AUTH0_CALLBACK_HOST = os.environ.get("AUTH0_CALLBACK_HOST", "127.0.0.1")
AUTH0_CALLBACK_PORT = int(os.environ.get("AUTH0_CALLBACK_PORT", "8765"))
AUTH0_SCOPE = os.environ.get("AUTH0_SCOPE", "openid profile email")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def generate_pkce_pair() -> tuple[str, str]:
    verifier = _b64url(secrets.token_bytes(32))
    challenge = _b64url(hashlib.sha256(verifier.encode()).digest())
    return verifier, challenge


def build_authorization_url(
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
    audience: Optional[str] = None,
    state: Optional[str] = None,
    code_challenge: Optional[str] = None,
    domain: Optional[str] = None,
) -> tuple[str, str]:
    client_id = client_id or AUTH0_CLIENT_ID
    redirect_uri = redirect_uri or f"http://{AUTH0_CALLBACK_HOST}:{AUTH0_CALLBACK_PORT}/callback"
    scope = scope or AUTH0_SCOPE
    audience = audience if audience is not None else AUTH0_AUDIENCE
    domain = domain or AUTH0_DOMAIN
    if not client_id or not domain:
        raise RuntimeError("AUTH0_DOMAIN and AUTH0_CLIENT_ID are required")
    verifier, challenge = generate_pkce_pair()
    if code_challenge is None:
        code_challenge = challenge
    if state is None:
        state = secrets.token_urlsafe(16)
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": state,
    }
    if audience:
        params["audience"] = audience
    return f"https://{domain}/authorize?{urlencode(params)}", verifier


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


def _start_local_server(host: Optional[str] = None, port: Optional[int] = None):
    server = HTTPServer((host or AUTH0_CALLBACK_HOST, port or AUTH0_CALLBACK_PORT), _CallbackHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def exchange_authorization_code(
    code: str,
    redirect_uri: str,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    code_verifier: Optional[str] = None,
    domain: Optional[str] = None,
) -> Dict[str, Any]:
    client_id = client_id or AUTH0_CLIENT_ID
    client_secret = client_secret or AUTH0_CLIENT_SECRET
    domain = domain or AUTH0_DOMAIN
    if not client_id or not domain:
        raise ValueError("AUTH0_DOMAIN and AUTH0_CLIENT_ID are required")
    payload: Dict[str, Any] = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier
    if client_secret:
        payload["client_secret"] = client_secret
    response = requests.post(f"https://{domain}/oauth/token", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def login(timeout_seconds: int = 300, redirect_uri: Optional[str] = None) -> Dict[str, Any]:
    auth_url, verifier = build_authorization_url(redirect_uri=redirect_uri)
    redirect_uri = redirect_uri or f"http://{AUTH0_CALLBACK_HOST}:{AUTH0_CALLBACK_PORT}/callback"
    server = _start_local_server()
    try:
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
        return exchange_authorization_code(
            code=_CallbackHandler.code,
            redirect_uri=redirect_uri,
            code_verifier=verifier,
        )
    finally:
        server.shutdown()
        server.server_close()


def fetch_profile_claims(access_token: str) -> Dict[str, Any]:
    response = requests.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )
    response.raise_for_status()
    claims = response.json()
    return {
        "provider": "google",
        "subject": claims.get("sub"),
        "email": claims.get("email"),
        "email_verified": claims.get("email_verified"),
        "full_name": claims.get("name"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "picture_url": claims.get("picture"),
        "locale": claims.get("locale"),
        "raw_claims": claims,
    }


def load_local_configuration(path: Optional[str] = None) -> Dict[str, Any]:
    config_path = path or os.environ.get("IDENTITY_CLIENT_CONFIG", "identity_client.json")
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r", encoding="utf-8") as fh:
        return json.load(fh)


@dataclass
class FederatedLoginClient:
    domain: str = AUTH0_DOMAIN or ""
    client_id: str = AUTH0_CLIENT_ID or ""
    client_secret: str = AUTH0_CLIENT_SECRET or ""
    audience: str = AUTH0_AUDIENCE or ""
    scope: str = AUTH0_SCOPE

    def authorization_url(self, redirect_uri: str) -> tuple[str, str]:
        return build_authorization_url(
            client_id=self.client_id or None,
            redirect_uri=redirect_uri,
            scope=self.scope,
            audience=self.audience or None,
            domain=self.domain or None,
        )

    def exchange_code(self, code: str, redirect_uri: str, code_verifier: Optional[str] = None) -> Dict[str, Any]:
        return exchange_authorization_code(
            code=code,
            redirect_uri=redirect_uri,
            client_id=self.client_id or None,
            client_secret=self.client_secret or None,
            code_verifier=code_verifier,
            domain=self.domain or None,
        )

    def login(self, timeout_seconds: int = 300, redirect_uri: Optional[str] = None) -> Dict[str, Any]:
        return login(timeout_seconds=timeout_seconds, redirect_uri=redirect_uri)
