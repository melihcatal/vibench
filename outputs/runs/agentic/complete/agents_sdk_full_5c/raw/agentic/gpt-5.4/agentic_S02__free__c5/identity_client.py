from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlencode

import requests


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_REDIRECT_URI_ENV = "AUTH0_REDIRECT_URI"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"


@dataclass(slots=True)
class Auth0Config:
    domain: str
    client_id: str
    client_secret: Optional[str]
    redirect_uri: str
    audience: Optional[str]

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
    def __init__(self, config: Optional[Auth0Config] = None, timeout: float = 15.0) -> None:
        self.config = config or load_auth0_config()
        self.timeout = timeout
        self.session = requests.Session()

    def build_authorize_url(
        self,
        *,
        state: str,
        scope: str,
        response_type: str = "code",
        audience: Optional[str] = None,
        nonce: Optional[str] = None,
        code_challenge: Optional[str] = None,
        code_challenge_method: Optional[str] = None,
        prompt: Optional[str] = None,
    ) -> str:
        params = {
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "response_type": response_type,
            "scope": scope,
            "state": state,
        }
        if audience or self.config.audience:
            params["audience"] = audience or self.config.audience
        if nonce:
            params["nonce"] = nonce
        if code_challenge:
            params["code_challenge"] = code_challenge
        if code_challenge_method:
            params["code_challenge_method"] = code_challenge_method
        if prompt:
            params["prompt"] = prompt
        return f"{self.config.authorize_url}?{urlencode(params)}"

    def exchange_code(self, code: str, *, code_verifier: Optional[str] = None) -> dict:
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.config.client_id,
            "code": code,
            "redirect_uri": self.config.redirect_uri,
        }
        if self.config.client_secret:
            payload["client_secret"] = self.config.client_secret
        if code_verifier:
            payload["code_verifier"] = code_verifier
        response = self.session.post(self.config.token_url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def fetch_userinfo(self, access_token: str) -> dict:
        response = self.session.get(
            self.config.userinfo_url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()


def load_auth0_config() -> Auth0Config:
    domain = os.environ[AUTH0_DOMAIN_ENV]
    client_id = os.environ[AUTH0_CLIENT_ID_ENV]
    redirect_uri = os.environ[AUTH0_REDIRECT_URI_ENV]
    client_secret = os.environ.get(AUTH0_CLIENT_SECRET_ENV)
    audience = os.environ.get(AUTH0_AUDIENCE_ENV)
    return Auth0Config(
        domain=domain,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        audience=audience,
    )


def generate_state() -> str:
    return secrets.token_urlsafe(32)


def generate_nonce() -> str:
    return secrets.token_urlsafe(32)


def generate_code_verifier() -> str:
    return secrets.token_urlsafe(64)


def generate_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
