from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from urllib.parse import urlencode

import requests

from identity_models import (
    OAuthCallbackRequest,
    OAuthLoginRequest,
    PKCELoginRequest,
    TokenBundle,
)


GOOGLE_AUTH_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


@dataclass
class GoogleOIDCConfig:
    client_id: str
    client_secret: str | None
    redirect_uri: str

    @classmethod
    def from_env(cls, redirect_uri: str | None = None) -> "GoogleOIDCConfig":
        return cls(
            client_id=os.environ["GOOGLE_CLIENT_ID"],
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
            redirect_uri=redirect_uri or os.environ["GOOGLE_REDIRECT_URI"],
        )


def build_authorization_url(
    config: GoogleOIDCConfig, request: OAuthLoginRequest
) -> str:
    query = urlencode(
        {
            "client_id": config.client_id,
            "redirect_uri": request.redirect_uri or config.redirect_uri,
            "response_type": "code",
            "scope": request.scope,
            "state": request.state,
            "prompt": request.prompt,
            "access_type": "offline",
            "include_granted_scopes": "true",
        }
    )
    return f"{GOOGLE_AUTH_BASE_URL}?{query}"


def generate_code_verifier(length: int = 64) -> str:
    verifier = secrets.token_urlsafe(length)
    return verifier[:128]


def build_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("utf-8")


def build_pkce_authorization_url(
    config: GoogleOIDCConfig, request: PKCELoginRequest
) -> str:
    query = urlencode(
        {
            "client_id": config.client_id,
            "redirect_uri": request.redirect_uri or config.redirect_uri,
            "response_type": "code",
            "scope": request.scope,
            "state": request.state,
            "prompt": request.prompt,
            "code_challenge": build_code_challenge(request.code_verifier),
            "code_challenge_method": "S256",
            "access_type": "offline",
        }
    )
    return f"{GOOGLE_AUTH_BASE_URL}?{query}"


def exchange_code_for_tokens(
    config: GoogleOIDCConfig, callback: OAuthCallbackRequest
) -> TokenBundle:
    payload = {
        "client_id": config.client_id,
        "code": callback.code,
        "redirect_uri": callback.redirect_uri or config.redirect_uri,
        "grant_type": "authorization_code",
    }
    if callback.code_verifier:
        payload["code_verifier"] = callback.code_verifier
    if config.client_secret:
        payload["client_secret"] = config.client_secret
    response = requests.post(GOOGLE_TOKEN_URL, data=payload, timeout=30)
    response.raise_for_status()
    token_data = response.json()
    return TokenBundle(
        access_token=token_data["access_token"],
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        token_type=token_data.get("token_type", "Bearer"),
        expires_in=token_data.get("expires_in"),
        scope=token_data.get("scope"),
        raw=token_data,
    )


def fetch_google_userinfo(access_token: str) -> dict:
    response = requests.get(
        GOOGLE_USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
