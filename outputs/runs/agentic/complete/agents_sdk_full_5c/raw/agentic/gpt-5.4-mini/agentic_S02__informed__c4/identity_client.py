from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import asdict
from typing import Any
from urllib.parse import urlencode

import requests

from identity_models import LoginRequest, TokenResponse

AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_REDIRECT_URI_ENV = "AUTH0_REDIRECT_URI"


def load_identity_config() -> dict[str, str]:
    return {
        "issuer": os.environ.get(AUTH0_DOMAIN_ENV, "https://example.auth0.com"),
        "client_id": os.environ.get(AUTH0_CLIENT_ID_ENV, "example-client-id"),
        "client_secret": os.environ.get(AUTH0_CLIENT_SECRET_ENV, "example-client-secret"),
        "redirect_uri": os.environ.get(AUTH0_REDIRECT_URI_ENV, "https://app.example.com/callback"),
    }


def auth0_authorize_url(request: LoginRequest, response_type: str = "code") -> str:
    base = f"https://{request.issuer}/authorize" if not request.issuer.startswith("https://") else f"{request.issuer}/authorize"
    params = {
        "response_type": response_type,
        "client_id": request.client_id,
        "redirect_uri": request.redirect_uri,
        "scope": request.scope,
    }
    if request.state:
        params["state"] = request.state
    if request.nonce:
        params["nonce"] = request.nonce
    return f"{base}?{urlencode(params)}"


def exchange_auth0_code(issuer: str, client_id: str, client_secret: str, code: str, redirect_uri: str) -> TokenResponse:
    token_url = f"https://{issuer}/oauth/token" if not issuer.startswith("https://") else f"{issuer}/oauth/token"
    resp = requests.post(
        token_url,
        json={
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
        },
        timeout=20,
    )
    resp.raise_for_status()
    payload: dict[str, Any] = resp.json()
    return TokenResponse(
        access_token=payload["access_token"],
        id_token=payload.get("id_token"),
        refresh_token=payload.get("refresh_token"),
        expires_in=payload.get("expires_in"),
        token_type=payload.get("token_type"),
    )


def make_pkce_pair() -> tuple[str, str]:
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip("=")
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
    return verifier, challenge


def authorize_with_pkce(issuer: str, client_id: str, redirect_uri: str, scope: str, state: str, nonce: str) -> dict[str, str]:
    verifier, challenge = make_pkce_pair()
    request = LoginRequest(issuer=issuer, client_id=client_id, redirect_uri=redirect_uri, scope=scope, state=state, nonce=nonce)
    return {
        "authorize_url": auth0_authorize_url(request) + f"&code_challenge={challenge}&code_challenge_method=S256",
        "code_verifier": verifier,
    }


def dump_config() -> dict[str, Any]:
    return asdict(load_identity_config())
