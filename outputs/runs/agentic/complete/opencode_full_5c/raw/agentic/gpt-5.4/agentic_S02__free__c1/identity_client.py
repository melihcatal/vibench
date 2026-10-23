from __future__ import annotations

import os
import secrets
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import requests

from identity_models import (
    OAuthCallbackRequest,
    OAuthStartRequest,
    PKCEStartRequest,
    TokenResponse,
)


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"


@dataclass
class Auth0Config:
    domain: str
    client_id: str
    client_secret: str | None = None
    audience: str | None = None

    @property
    def issuer(self) -> str:
        return f"https://{self.domain}/"

    @property
    def authorize_url(self) -> str:
        return f"https://{self.domain}/authorize"

    @property
    def token_url(self) -> str:
        return f"https://{self.domain}/oauth/token"

    @property
    def userinfo_url(self) -> str:
        return f"https://{self.domain}/userinfo"


def load_auth0_config() -> Auth0Config:
    domain = os.environ[AUTH0_DOMAIN_ENV]
    client_id = os.environ[AUTH0_CLIENT_ID_ENV]
    client_secret = os.getenv(AUTH0_CLIENT_SECRET_ENV)
    audience = os.getenv(AUTH0_AUDIENCE_ENV)
    return Auth0Config(
        domain=domain,
        client_id=client_id,
        client_secret=client_secret,
        audience=audience,
    )


def build_authorization_url(
    request: OAuthStartRequest, config: Auth0Config | None = None
) -> str:
    cfg = config or load_auth0_config()
    query: dict[str, Any] = {
        "response_type": "code",
        "client_id": cfg.client_id,
        "redirect_uri": request.redirect_uri,
        "scope": request.scope,
        "state": request.state,
    }
    audience = request.audience or cfg.audience
    if audience:
        query["audience"] = audience
    if request.prompt:
        query["prompt"] = request.prompt
    return f"{cfg.authorize_url}?{urlencode(query)}"


def build_pkce_authorization_url(
    request: PKCEStartRequest, config: Auth0Config | None = None
) -> str:
    cfg = config or load_auth0_config()
    query: dict[str, Any] = {
        "response_type": "code",
        "client_id": cfg.client_id,
        "redirect_uri": request.redirect_uri,
        "scope": request.scope,
        "state": request.state,
        "code_challenge": request.code_challenge,
        "code_challenge_method": request.code_challenge_method,
    }
    audience = request.audience or cfg.audience
    if audience:
        query["audience"] = audience
    return f"{cfg.authorize_url}?{urlencode(query)}"


def exchange_code_for_tokens(
    request: OAuthCallbackRequest, config: Auth0Config | None = None
) -> TokenResponse:
    cfg = config or load_auth0_config()
    payload: dict[str, Any] = {
        "grant_type": "authorization_code",
        "client_id": cfg.client_id,
        "code": request.code,
        "redirect_uri": request.redirect_uri,
    }
    if cfg.client_secret:
        payload["client_secret"] = cfg.client_secret
    if request.code_verifier:
        payload["code_verifier"] = request.code_verifier
    response = requests.post(cfg.token_url, json=payload, timeout=30)
    response.raise_for_status()
    body = response.json()
    return TokenResponse(
        access_token=body["access_token"],
        id_token=body.get("id_token"),
        refresh_token=body.get("refresh_token"),
        token_type=body.get("token_type", "Bearer"),
        expires_in=body.get("expires_in"),
        scope=body.get("scope"),
        raw=body,
    )


def fetch_auth0_userinfo(
    access_token: str, config: Auth0Config | None = None
) -> dict[str, Any]:
    cfg = config or load_auth0_config()
    response = requests.get(
        cfg.userinfo_url,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def generate_state(prefix: str = "st") -> str:
    return f"{prefix}_{secrets.token_urlsafe(24)}"
