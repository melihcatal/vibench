from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import requests

from identity_models import TokenExchangeRequest, TokenSet, normalize_scopes


GOOGLE_AUTH_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


@dataclass(slots=True)
class GoogleOIDCConfig:
    client_id: str
    client_secret: str | None
    default_redirect_uri: str


def load_google_oidc_config() -> GoogleOIDCConfig:
    client_id = os.environ["GOOGLE_CLIENT_ID"]
    redirect_uri = os.environ["GOOGLE_REDIRECT_URI"]
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    return GoogleOIDCConfig(
        client_id=client_id,
        client_secret=client_secret,
        default_redirect_uri=redirect_uri,
    )


def build_google_authorization_url(
    *,
    redirect_uri: str,
    state: str,
    scopes: list[str] | str,
    access_type: str = "offline",
    include_granted_scopes: bool = True,
    prompt: str | None = None,
    login_hint: str | None = None,
    code_challenge: str | None = None,
    nonce: str | None = None,
) -> str:
    config = load_google_oidc_config()
    params: dict[str, Any] = {
        "client_id": config.client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": normalize_scopes(scopes),
        "state": state,
        "access_type": access_type,
        "include_granted_scopes": "true" if include_granted_scopes else "false",
    }
    if prompt:
        params["prompt"] = prompt
    if login_hint:
        params["login_hint"] = login_hint
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    if nonce:
        params["nonce"] = nonce
    return f"{GOOGLE_AUTH_BASE_URL}?{urlencode(params)}"


def generate_pkce_verifier(length: int = 64) -> str:
    token = secrets.token_urlsafe(length)
    return token[:128]


def pkce_s256_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def exchange_google_code(request: TokenExchangeRequest) -> TokenSet:
    config = load_google_oidc_config()
    payload: dict[str, Any] = {
        "client_id": config.client_id,
        "code": request.code,
        "redirect_uri": request.redirect_uri,
        "grant_type": "authorization_code",
    }
    if config.client_secret:
        payload["client_secret"] = config.client_secret
    if request.code_verifier:
        payload["code_verifier"] = request.code_verifier
    response = requests.post(GOOGLE_TOKEN_URL, data=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return TokenSet(
        access_token=data["access_token"],
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        token_type=data.get("token_type", "Bearer"),
        expires_in=data.get("expires_in"),
        scope=data.get("scope"),
        provider="google_oidc",
        raw=data,
    )


def fetch_google_userinfo(access_token: str) -> dict[str, Any]:
    response = requests.get(
        GOOGLE_USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
