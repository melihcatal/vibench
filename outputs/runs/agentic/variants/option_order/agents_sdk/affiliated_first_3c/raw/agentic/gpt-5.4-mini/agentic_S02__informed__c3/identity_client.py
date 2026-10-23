from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import asdict
from typing import Any
from urllib.parse import urlencode

import requests

from identity_models import AuthorizationRequest, TokenExchangeRequest, TokenSet

AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_REDIRECT_URI_ENV = "AUTH0_REDIRECT_URI"
AUTH0_ISSUER_ENV = "AUTH0_ISSUER"


def load_auth0_config() -> dict[str, str]:
    domain = os.getenv(AUTH0_DOMAIN_ENV, "")
    client_id = os.getenv(AUTH0_CLIENT_ID_ENV, "")
    client_secret = os.getenv(AUTH0_CLIENT_SECRET_ENV, "")
    redirect_uri = os.getenv(AUTH0_REDIRECT_URI_ENV, "https://example.com/callback")
    issuer = os.getenv(AUTH0_ISSUER_ENV, f"https://{domain}/") if domain else ""
    return {
        "domain": domain,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "issuer": issuer,
    }


def auth0_authorize_url(req: AuthorizationRequest) -> str:
    return f"{req.issuer.rstrip('/')}/authorize?" + urlencode({k: v for k, v in asdict(req).items() if v})


def oauth2_token_endpoint(issuer: str) -> str:
    return f"{issuer.rstrip('/')}/oauth/token"


def exchange_code(req: TokenExchangeRequest) -> TokenSet:
    payload: dict[str, Any] = {
        "grant_type": "authorization_code",
        "client_id": req.client_id,
        "code": req.code,
        "redirect_uri": req.redirect_uri,
    }
    if req.client_secret:
        payload["client_secret"] = req.client_secret
    if req.code_verifier:
        payload["code_verifier"] = req.code_verifier
    resp = requests.post(oauth2_token_endpoint(req.issuer), json=payload, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return TokenSet(
        access_token=str(data.get("access_token", "")),
        id_token=str(data.get("id_token", "")),
        refresh_token=str(data.get("refresh_token", "")),
        token_type=str(data.get("token_type", "Bearer")),
        expires_in=int(data.get("expires_in", 0) or 0),
        raw=data,
    )


def make_pkce_pair() -> tuple[str, str]:
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip("=")
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
    return verifier, challenge
