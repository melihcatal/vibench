import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Any

GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def create_state() -> str:
    return secrets.token_urlsafe(24)


def create_nonce() -> str:
    return secrets.token_urlsafe(24)


def create_code_verifier() -> str:
    return secrets.token_urlsafe(48)


def create_code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return _b64url(digest)


def get_google_client_config() -> dict[str, str]:
    return {
        "client_id": os.environ.get("GOOGLE_CLIENT_ID", ""),
        "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET", ""),
        "redirect_uri": os.environ.get("GOOGLE_REDIRECT_URI", ""),
        "issuer": "https://accounts.google.com",
    }


def build_authorization_url(client_id: str, redirect_uri: str, state: str, nonce: str, scopes: list[str], code_challenge: str | None = None) -> str:
    from urllib.parse import urlencode

    params: dict[str, Any] = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(scopes),
        "state": state,
        "nonce": nonce,
        "access_type": "offline",
        "prompt": "consent",
    }
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    return f"{GOOGLE_AUTH_ENDPOINT}?{urlencode(params)}"


def exchange_code_for_tokens(code: str, redirect_uri: str, client_id: str, client_secret: str, code_verifier: str | None = None) -> dict[str, Any]:
    import requests

    data: dict[str, Any] = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    response = requests.post(GOOGLE_TOKEN_ENDPOINT, data=data, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_google_userinfo(access_token: str) -> dict[str, Any]:
    import requests

    response = requests.get(GOOGLE_USERINFO_ENDPOINT, headers={"Authorization": f"Bearer {access_token}"}, timeout=30)
    response.raise_for_status()
    return response.json()


@dataclass
class IdentitySession:
    state: str
    nonce: str
    code_verifier: str = ""
