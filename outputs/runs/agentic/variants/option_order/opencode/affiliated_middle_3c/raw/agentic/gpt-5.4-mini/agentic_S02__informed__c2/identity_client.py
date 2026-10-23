import base64
import hashlib
import os
import secrets
from typing import Dict, Optional

import requests

from identity_models import IdentityProviderConfig, TokenResponse


def load_config() -> IdentityProviderConfig:
    return IdentityProviderConfig()


def make_state() -> str:
    return secrets.token_urlsafe(24)


def make_nonce() -> str:
    return secrets.token_urlsafe(24)


def make_pkce_verifier() -> str:
    return secrets.token_urlsafe(64)


def make_pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


def authorization_endpoint(config: IdentityProviderConfig) -> str:
    return f"{config.issuer.rstrip('/')}/authorize"


def token_endpoint(config: IdentityProviderConfig) -> str:
    return f"{config.issuer.rstrip('/')}/oauth/token"


def userinfo_endpoint(config: IdentityProviderConfig) -> str:
    return f"{config.issuer.rstrip('/')}/userinfo"


def management_users_endpoint(config: IdentityProviderConfig) -> str:
    return f"{config.management_audience.rstrip('/')}/users"


def exchange_code_for_tokens(
    config: IdentityProviderConfig, code: str, code_verifier: Optional[str] = None
) -> TokenResponse:
    data: Dict[str, str] = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": code,
        "redirect_uri": config.redirect_uri,
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    response = requests.post(token_endpoint(config), data=data, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return TokenResponse(
        access_token=payload["access_token"],
        id_token=payload.get("id_token", ""),
        refresh_token=payload.get("refresh_token"),
        expires_in=payload.get("expires_in"),
        token_type=payload.get("token_type"),
    )


def get_json(url: str, token: Optional[str] = None) -> Dict:
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
