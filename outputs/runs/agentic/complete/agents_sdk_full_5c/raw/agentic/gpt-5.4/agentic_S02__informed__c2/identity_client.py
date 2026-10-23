from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Dict, Optional
from urllib.parse import urlencode

import requests


AUTH0_OAUTH_AUTHORIZE_PATH = "/authorize"
AUTH0_OAUTH_TOKEN_PATH = "/oauth/token"
AUTH0_USERINFO_PATH = "/userinfo"


@dataclass
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
    def authorization_endpoint(self) -> str:
        return f"https://{self.domain}{AUTH0_OAUTH_AUTHORIZE_PATH}"

    @property
    def token_endpoint(self) -> str:
        return f"https://{self.domain}{AUTH0_OAUTH_TOKEN_PATH}"

    @property
    def userinfo_endpoint(self) -> str:
        return f"https://{self.domain}{AUTH0_USERINFO_PATH}"


class Auth0OIDCClient:
    def __init__(self, config: Optional[Auth0Config] = None) -> None:
        self.config = config or load_auth0_config()
        self._session = requests.Session()

    def build_authorization_url(
        self,
        redirect_uri: str,
        scope: Optional[str] = None,
        state: Optional[str] = None,
        nonce: Optional[str] = None,
        audience: Optional[str] = None,
        prompt: Optional[str] = None,
        code_challenge: Optional[str] = None,
        code_challenge_method: Optional[str] = None,
    ) -> str:
        params: Dict[str, str] = {
            "response_type": "code",
            "client_id": self.config.client_id,
            "redirect_uri": redirect_uri,
            "scope": scope or self.config.default_scope,
            "state": state or generate_state(),
            "nonce": nonce or generate_nonce(),
        }
        selected_audience = audience or self.config.audience
        if selected_audience:
            params["audience"] = selected_audience
        if prompt:
            params["prompt"] = prompt
        if code_challenge:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = code_challenge_method or "S256"
        return f"{self.config.authorization_endpoint}?{urlencode(params)}"

    def exchange_code(
        self,
        code: str,
        redirect_uri: str,
        code_verifier: Optional[str] = None,
    ) -> Dict[str, object]:
        payload: Dict[str, str] = {
            "grant_type": "authorization_code",
            "client_id": self.config.client_id,
            "code": code,
            "redirect_uri": redirect_uri,
        }
        if self.config.client_secret:
            payload["client_secret"] = self.config.client_secret
        if code_verifier:
            payload["code_verifier"] = code_verifier
        response = self._session.post(self.config.token_endpoint, data=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def fetch_userinfo(self, access_token: str) -> Dict[str, object]:
        response = self._session.get(
            self.config.userinfo_endpoint,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


def load_auth0_config() -> Auth0Config:
    domain = os.environ["AUTH0_DOMAIN"]
    client_id = os.environ["AUTH0_CLIENT_ID"]
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
    audience = os.environ.get("AUTH0_AUDIENCE")
    return Auth0Config(
        domain=domain,
        client_id=client_id,
        client_secret=client_secret,
        audience=audience,
    )


def generate_state() -> str:
    return secrets.token_urlsafe(24)


def generate_nonce() -> str:
    return secrets.token_urlsafe(24)


def generate_code_verifier() -> str:
    return secrets.token_urlsafe(64)


def generate_pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
