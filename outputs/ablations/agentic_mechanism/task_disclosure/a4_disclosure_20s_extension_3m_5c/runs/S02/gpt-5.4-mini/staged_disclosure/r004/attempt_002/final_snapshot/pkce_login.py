import base64
import hashlib
import json
import os
import secrets
import sys
import urllib.parse
import webbrowser

import requests


AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
REDIRECT_URI = os.environ.get("GOOGLE_OAUTH_REDIRECT_URI", "http://localhost:8080/callback")
SCOPE = os.environ.get("GOOGLE_OAUTH_SCOPE", "openid email profile")


def _code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def _authorization_url(state: str, code_verifier: str) -> str:
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "state": state,
        "code_challenge": _code_challenge(code_verifier),
        "code_challenge_method": "S256",
        "access_type": "offline",
        "prompt": "consent",
    }
    return f"{AUTHORIZATION_ENDPOINT}?{urllib.parse.urlencode(params)}"


def pkce_login() -> dict:
    if not CLIENT_ID:
        raise RuntimeError("GOOGLE_OAUTH_CLIENT_ID is required")

    state = secrets.token_urlsafe(24)
    code_verifier = secrets.token_urlsafe(64)
    auth_url = _authorization_url(state, code_verifier)
    webbrowser.open(auth_url)
    callback_url = input("Paste the full callback URL: ").strip()
    parsed = urllib.parse.urlparse(callback_url)
    params = urllib.parse.parse_qs(parsed.query)

    if params.get("state", [None])[0] != state:
        raise RuntimeError("state mismatch")

    code = params.get("code", [None])[0]
    if not code:
        raise RuntimeError("authorization code missing")

    response = requests.post(
        TOKEN_ENDPOINT,
        data={
            "client_id": CLIENT_ID,
            "code": code,
            "code_verifier": code_verifier,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    sys.stdout.write(json.dumps(pkce_login()))
