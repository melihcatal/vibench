from __future__ import annotations

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
AUTH0_REDIRECT_URI_ENV = "AUTH0_REDIRECT_URI"
AUTH0_SCOPES_ENV = "AUTH0_SCOPES"


@dataclass(slots=True)
class Auth0Config:
    domain: str
    client_id: str
    client_secret: Optional[str]
    redirect_uri: str
    audience: Optional[str] = None
    scopes: str = "openid profile email"

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


class Auth0Client:
    def __init__(self, config: Auth0Config, session: Optional[requests.Session] = None) -> None:
        self.config = config
        self.session = session or requests.Session()

    def build_authorization_url(
        self,
        state: str,
        nonce: Optional[str] = None,
        code_challenge: Optional[str] = None,
        code_challenge_method: Optional[str] = None,
        prompt: Optional[str] = None,
    ) -> str:
        query: Dict[str, str] = {
            "response_type": "code",
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "scope": self.config.scopes,
            "state": state,
        }
        if self.config.audience:
            query["audience"] = self.config.audience
        if nonce:
            query["nonce"] = nonce
        if code_challenge:
            query["code_challenge"] = code_challenge
        if code_challenge_method:
            query["code_challenge_method"] = code_challenge_method
        if prompt:
            query["prompt"] = prompt
        return f"{self.config.authorization_endpoint}?{urlencode(query)}"

    def exchange_code(self, code: str, code_verifier: Optional[str] = None) -> dict:
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
        response = self.session.post(self.config.token_endpoint, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()

    def fetch_userinfo(self, access_token: str) -> dict:
        response = self.session.get(
            self.config.userinfo_endpoint,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=15,
        )
        response.raise_for_status()
        return response.json()


def load_auth0_config(public_client: bool = False) -> Auth0Config:
    client_secret = None if public_client else os.getenv(AUTH0_CLIENT_SECRET_ENV)
    return Auth0Config(
        domain=os.environ[AUTH0_DOMAIN_ENV],
        client_id=os.environ[AUTH0_CLIENT_ID_ENV],
        client_secret=client_secret,
        redirect_uri=os.environ[AUTH0_REDIRECT_URI_ENV],
        audience=os.getenv(AUTH0_AUDIENCE_ENV),
        scopes=os.getenv(AUTH0_SCOPES_ENV, "openid profile email"),
    )


def new_state_token() -> str:
    return secrets.token_urlsafe(24)


def new_nonce() -> str:
    return secrets.token_urlsafe(24)
