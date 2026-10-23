import base64
import hashlib
import os
import secrets
from typing import Any, Dict, Optional

import requests


GOOGLE_ISSUER = "https://accounts.google.com"


def get_identity_settings() -> Dict[str, str]:
    return {
        "issuer": os.getenv("GOOGLE_ISSUER", GOOGLE_ISSUER),
        "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
        "redirect_uri": os.getenv(
            "GOOGLE_REDIRECT_URI", "http://localhost:8080/oauth/callback"
        ),
        "user_info_url": os.getenv(
            "GOOGLE_USERINFO_URL", "https://openidconnect.googleapis.com/v1/userinfo"
        ),
        "token_url": os.getenv(
            "GOOGLE_TOKEN_URL", "https://oauth2.googleapis.com/token"
        ),
        "auth_url": os.getenv(
            "GOOGLE_AUTH_URL", "https://accounts.google.com/o/oauth2/v2/auth"
        ),
    }


def build_authorization_url(
    state: str, nonce: Optional[str] = None, code_challenge: Optional[str] = None
) -> str:
    settings = get_identity_settings()
    params = [
        ("client_id", settings["client_id"]),
        ("redirect_uri", settings["redirect_uri"]),
        ("response_type", "code"),
        ("scope", "openid profile email"),
        ("state", state),
    ]
    if nonce:
        params.append(("nonce", nonce))
    if code_challenge:
        params.extend(
            [("code_challenge", code_challenge), ("code_challenge_method", "S256")]
        )
    return (
        settings["auth_url"]
        + "?"
        + "&".join(f"{k}={requests.utils.quote(v)}" for k, v in params if v)
    )


def generate_state() -> str:
    return secrets.token_urlsafe(24)


def generate_nonce() -> str:
    return secrets.token_urlsafe(24)


def generate_pkce_verifier() -> str:
    return secrets.token_urlsafe(64)


def generate_pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def exchange_code(
    code: str, redirect_uri: Optional[str] = None, code_verifier: Optional[str] = None
) -> Dict[str, Any]:
    settings = get_identity_settings()
    data = {
        "client_id": settings["client_id"],
        "client_secret": settings["client_secret"],
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri or settings["redirect_uri"],
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    response = requests.post(settings["token_url"], data=data, timeout=20)
    response.raise_for_status()
    return response.json()


def fetch_userinfo(access_token: str) -> Dict[str, Any]:
    settings = get_identity_settings()
    response = requests.get(
        settings["user_info_url"],
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()
