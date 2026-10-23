import base64
import hashlib
import json
import os
import secrets
import urllib.parse
import urllib.request


AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost")
SCOPES = os.environ.get("GOOGLE_OAUTH_SCOPES", "openid email profile")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def generate_pkce_pair() -> tuple[str, str]:
    verifier = _b64url(secrets.token_bytes(32))
    challenge = _b64url(hashlib.sha256(verifier.encode("ascii")).digest())
    return verifier, challenge


def build_authorization_url(state: str | None = None) -> tuple[str, str, str]:
    if not CLIENT_ID:
        raise ValueError("GOOGLE_CLIENT_ID is required")
    verifier, challenge = generate_pkce_pair()
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "access_type": "offline",
        "include_granted_scopes": "true",
    }
    if state is None:
        state = _b64url(secrets.token_bytes(16))
    params["state"] = state
    return f"{AUTHORIZATION_ENDPOINT}?{urllib.parse.urlencode(params)}", verifier, state


def exchange_code_for_tokens(code: str, code_verifier: str) -> dict:
    if not CLIENT_ID:
        raise ValueError("GOOGLE_CLIENT_ID is required")
    payload = urllib.parse.urlencode(
        {
            "client_id": CLIENT_ID,
            "grant_type": "authorization_code",
            "code": code,
            "code_verifier": code_verifier,
            "redirect_uri": REDIRECT_URI,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        TOKEN_ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def login_with_pkce(authorization_code: str) -> dict:
    _, verifier, _ = build_authorization_url()
    return exchange_code_for_tokens(authorization_code, verifier)
