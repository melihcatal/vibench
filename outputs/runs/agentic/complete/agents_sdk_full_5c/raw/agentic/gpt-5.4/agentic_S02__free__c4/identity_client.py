from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Dict, Optional
from urllib.parse import urlencode

import requests


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"
AUTH0_DEFAULT_SCOPE_ENV = "AUTH0_DEFAULT_SCOPE"
AUTH0_MANAGEMENT_API_AUDIENCE = "https://{domain}/api/v2/"


@dataclass(slots=True)
class Auth0Config:
    domain: str
    client_id: str
    client_secret: Optional[str] = None
    audience: Optional[str] = None
    default_scope: str = "openid profile email"

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


class Auth0Client:
    def __init__(self, config: Optional[Auth0Config] = None, session: Optional[requests.Session] = None) -> None:
        self.config = config or load_auth0_config()
        self.session = session or requests.Session()

    def build_authorization_url(
        self,
        redirect_uri: str,
        state: str,
        scope: Optional[str] = None,
        prompt: Optional[str] = None,
        login_hint: Optional[str] = None,
        nonce: Optional[str] = None,
        code_challenge: Optional[str] = None,
        code_challenge_method: Optional[str] = None,
        audience: Optional[str] = None,
    ) -> str:
        params: Dict[str, str] = {
            "response_type": "code",
            "client_id": self.config.client_id,
            "redirect_uri": redirect_uri,
            "scope": scope or self.config.default_scope,
            "state": state,
        }
        if prompt:
            params["prompt"] = prompt
        if login_hint:
            params["login_hint"] = login_hint
        if nonce:
            params["nonce"] = nonce
        if code_challenge:
            params["code_challenge"] = code_challenge
        if code_challenge_method:
            params["code_challenge_method"] = code_challenge_method
        effective_audience = audience or self.config.audience
        if effective_audience:
            params["audience"] = effective_audience
        return f"{self.config.authorize_url}?{urlencode(params)}"

    def exchange_code(
        self,
        code: str,
        redirect_uri: str,
        code_verifier: Optional[str] = None,
    ) -> dict:
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.config.client_id,
            "code": code,
            "redirect_uri": redirect_uri,
        }
        if self.config.client_secret:
            payload["client_secret"] = self.config.client_secret
        if code_verifier:
            payload["code_verifier"] = code_verifier
        response = self.session.post(self.config.token_url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def userinfo(self, access_token: str) -> dict:
        response = self.session.get(
            self.config.userinfo_url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


def load_auth0_config() -> Auth0Config:
    domain = os.environ[AUTH0_DOMAIN_ENV]
    client_id = os.environ[AUTH0_CLIENT_ID_ENV]
    client_secret = os.getenv(AUTH0_CLIENT_SECRET_ENV)
    audience = os.getenv(AUTH0_AUDIENCE_ENV)
    default_scope = os.getenv(AUTH0_DEFAULT_SCOPE_ENV, "openid profile email")
    return Auth0Config(
        domain=domain,
        client_id=client_id,
        client_secret=client_secret,
        audience=audience,
        default_scope=default_scope,
    )


def generate_state(length: int = 32) -> str:
    return secrets.token_urlsafe(length)


def generate_nonce(length: int = 32) -> str:
    return secrets.token_urlsafe(length)


def generate_code_verifier(length: int = 64) -> str:
    raw = secrets.token_urlsafe(length)
    return raw[:128]


def build_pkce_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
