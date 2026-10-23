from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Optional
from urllib.parse import urlencode

import requests

from identity_models import LoginRequest, TokenResponse


@dataclass
class IdentityProviderConfig:
    issuer: str
    client_id: str
    client_secret: str = ""
    redirect_uri: str = ""
    auth_endpoint: str = ""
    token_endpoint: str = ""
    userinfo_endpoint: str = ""


def load_identity_config(prefix: str = "AUTH0") -> IdentityProviderConfig:
    issuer = os.getenv(f"{prefix}_DOMAIN", "https://example.auth0.com")
    client_id = os.getenv(f"{prefix}_CLIENT_ID", "")
    client_secret = os.getenv(f"{prefix}_CLIENT_SECRET", "")
    redirect_uri = os.getenv(f"{prefix}_REDIRECT_URI", "https://app.example.com/callback")
    auth_endpoint = os.getenv(f"{prefix}_AUTHORIZE_URL", f"{issuer}/authorize")
    token_endpoint = os.getenv(f"{prefix}_TOKEN_URL", f"{issuer}/oauth/token")
    userinfo_endpoint = os.getenv(f"{prefix}_USERINFO_URL", f"{issuer}/userinfo")
    return IdentityProviderConfig(
        issuer=issuer,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        auth_endpoint=auth_endpoint,
        token_endpoint=token_endpoint,
        userinfo_endpoint=userinfo_endpoint,
    )


def build_authorize_url(config: IdentityProviderConfig, req: LoginRequest, code_challenge: str = "", code_challenge_method: str = "") -> str:
    params: Dict[str, str] = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": req.redirect_uri or config.redirect_uri,
        "scope": req.scope,
        "state": req.state,
        "nonce": req.nonce,
    }
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = code_challenge_method or "S256"
    return f"{config.auth_endpoint}?{urlencode({k: v for k, v in params.items() if v})}"


def exchange_code_for_tokens(config: IdentityProviderConfig, code: str, code_verifier: str = "") -> TokenResponse:
    payload = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": code,
        "redirect_uri": config.redirect_uri,
        "code_verifier": code_verifier,
    }
    resp = requests.post(config.token_endpoint, data=payload, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    return TokenResponse(
        access_token=data.get("access_token", ""),
        id_token=data.get("id_token", ""),
        refresh_token=data.get("refresh_token", ""),
        token_type=data.get("token_type", "Bearer"),
        expires_in=int(data.get("expires_in", 0)),
    )


def fetch_userinfo(config: IdentityProviderConfig, access_token: str) -> Dict[str, object]:
    resp = requests.get(config.userinfo_endpoint, headers={"Authorization": f"Bearer {access_token}"}, timeout=20)
    resp.raise_for_status()
    return resp.json()
