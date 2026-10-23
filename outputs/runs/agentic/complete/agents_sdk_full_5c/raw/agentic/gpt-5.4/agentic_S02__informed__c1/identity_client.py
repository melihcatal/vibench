from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import requests

from identity_models import OAuthStartRequest


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"
AUTH0_ISSUER_ENV = "AUTH0_ISSUER"


@dataclass(slots=True)
class Auth0Config:
    domain: str
    client_id: str
    client_secret: str | None = None
    audience: str | None = None
    issuer: str | None = None
    timeout: float = 15.0

    @property
    def base_url(self) -> str:
        domain = self.domain.strip().rstrip("/")
        if domain.startswith("https://"):
            return domain
        return f"https://{domain}"

    @property
    def resolved_issuer(self) -> str:
        return self.issuer or f"{self.base_url}/"

    @property
    def authorize_url(self) -> str:
        return f"{self.base_url}/authorize"

    @property
    def token_url(self) -> str:
        return f"{self.base_url}/oauth/token"

    @property
    def userinfo_url(self) -> str:
        return f"{self.base_url}/userinfo"


class Auth0OIDCClient:
    def __init__(self, config: Auth0Config):
        self.config = config

    def build_authorization_url(
        self,
        request: OAuthStartRequest,
        *,
        state: str,
        nonce: str,
        code_challenge: str | None = None,
        code_challenge_method: str | None = None,
    ) -> str:
        params: dict[str, Any] = {
            "response_type": "code",
            "client_id": self.config.client_id,
            "redirect_uri": request.redirect_uri,
            "scope": request.scope,
            "state": state,
            "nonce": nonce,
        }
        audience = request.audience or self.config.audience
        if audience:
            params["audience"] = audience
        if request.prompt:
            params["prompt"] = request.prompt
        if code_challenge:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = code_challenge_method or "S256"
        return f"{self.config.authorize_url}?{urlencode(params)}"

    def exchange_code(
        self,
        *,
        code: str,
        redirect_uri: str,
        code_verifier: str | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "grant_type": "authorization_code",
            "client_id": self.config.client_id,
            "code": code,
            "redirect_uri": redirect_uri,
        }
        if self.config.client_secret:
            payload["client_secret"] = self.config.client_secret
        if code_verifier:
            payload["code_verifier"] = code_verifier
        response = requests.post(self.config.token_url, json=payload, timeout=self.config.timeout)
        response.raise_for_status()
        return response.json()

    def fetch_userinfo(self, access_token: str) -> dict[str, Any]:
        response = requests.get(
            self.config.userinfo_url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        return response.json()


def load_auth0_config() -> Auth0Config:
    domain = os.environ[AUTH0_DOMAIN_ENV]
    client_id = os.environ[AUTH0_CLIENT_ID_ENV]
    client_secret = os.getenv(AUTH0_CLIENT_SECRET_ENV)
    audience = os.getenv(AUTH0_AUDIENCE_ENV)
    issuer = os.getenv(AUTH0_ISSUER_ENV)
    return Auth0Config(
        domain=domain,
        client_id=client_id,
        client_secret=client_secret,
        audience=audience,
        issuer=issuer,
    )


def generate_state() -> str:
    return secrets.token_urlsafe(24)


def generate_nonce() -> str:
    return secrets.token_urlsafe(24)


def generate_code_verifier() -> str:
    return secrets.token_urlsafe(64)


def build_pkce_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
