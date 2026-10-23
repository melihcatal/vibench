from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional
from urllib.parse import urlencode

import requests

from identity_models import CallbackRequest, OAuthLoginRequest, PKCELoginRequest


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"


@dataclass
class Auth0Config:
    domain: str
    client_id: str
    client_secret: Optional[str] = None
    audience: Optional[str] = None

    @property
    def issuer(self) -> str:
        return f"https://{self.domain}/"

    @property
    def authorization_endpoint(self) -> str:
        return f"https://{self.domain}/authorize"

    @property
    def token_endpoint(self) -> str:
        return f"https://{self.domain}/oauth/token"

    @property
    def userinfo_endpoint(self) -> str:
        return f"https://{self.domain}/userinfo"


def load_auth0_config() -> Auth0Config:
    domain = os.environ[AUTH0_DOMAIN_ENV]
    client_id = os.environ[AUTH0_CLIENT_ID_ENV]
    client_secret = os.environ.get(AUTH0_CLIENT_SECRET_ENV)
    audience = os.environ.get(AUTH0_AUDIENCE_ENV)
    return Auth0Config(
        domain=domain,
        client_id=client_id,
        client_secret=client_secret,
        audience=audience,
    )


def generate_state(size: int = 32) -> str:
    return secrets.token_urlsafe(size)


def generate_nonce(size: int = 32) -> str:
    return secrets.token_urlsafe(size)


def generate_code_verifier(size: int = 64) -> str:
    return secrets.token_urlsafe(size)[:128]


def build_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


def build_authorization_url(
    request: OAuthLoginRequest, *, use_pkce: bool = False
) -> str:
    config = load_auth0_config()
    params: Dict[str, Any] = {
        "client_id": config.client_id,
        "response_type": "code",
        **request.to_params(),
    }
    if config.audience:
        params["audience"] = config.audience
    if use_pkce and isinstance(request, PKCELoginRequest):
        params.update(
            {
                "code_challenge": request.code_challenge,
                "code_challenge_method": request.code_challenge_method,
            }
        )
    return f"{config.authorization_endpoint}?{urlencode(params)}"


def exchange_code_for_tokens(callback: CallbackRequest) -> Dict[str, Any]:
    config = load_auth0_config()
    payload: Dict[str, Any] = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "code": callback.code,
        "redirect_uri": callback.redirect_uri,
    }
    if callback.code_verifier:
        payload["code_verifier"] = callback.code_verifier
    if config.client_secret:
        payload["client_secret"] = config.client_secret
    response = requests.post(config.token_endpoint, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_userinfo(access_token: str) -> Dict[str, Any]:
    config = load_auth0_config()
    response = requests.get(
        config.userinfo_endpoint,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def bearer_headers(token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def ensure_scopes(scopes: Optional[Iterable[str]]) -> list[str]:
    final_scopes = ["openid", "profile", "email"]
    if scopes:
        for scope in scopes:
            if scope not in final_scopes:
                final_scopes.append(scope)
    return final_scopes
