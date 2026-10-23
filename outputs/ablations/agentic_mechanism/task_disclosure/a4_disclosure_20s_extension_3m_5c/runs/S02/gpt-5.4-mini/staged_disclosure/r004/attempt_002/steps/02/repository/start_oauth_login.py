import base64
import hashlib
import os
import secrets
import sys
import urllib.parse
import webbrowser

import requests


AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("GOOGLE_OAUTH_REDIRECT_URI", "http://localhost:8080/callback")
SCOPE = os.environ.get("GOOGLE_OAUTH_SCOPE", "openid email profile")


def _code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def _build_authorization_url(state: str, code_verifier: str) -> str:
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


def start_oauth_login() -> str:
    if not CLIENT_ID:
        raise RuntimeError("GOOGLE_OAUTH_CLIENT_ID is required")
    state = secrets.token_urlsafe(24)
    code_verifier = secrets.token_urlsafe(64)
    auth_url = _build_authorization_url(state, code_verifier)
    webbrowser.open(auth_url)
    code = input("Enter the authorization code: ").strip()
    token_response = requests.post(
        TOKEN_ENDPOINT,
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "code_verifier": code_verifier,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
        },
        timeout=30,
    )
    token_response.raise_for_status()
    return token_response.text


if __name__ == "__main__":
    try:
        sys.stdout.write(start_oauth_login())
    except Exception as exc:
        sys.stderr.write(f"error: {exc}\n")
        raise
