from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from identity_models import CallbackRequest, OAuthStartRequest, TokenSet, normalize_scope


AUTH0_DEFAULT_SCOPE = "openid profile email"


@dataclass
class Auth0Config:
    domain: str
    client_id: str
    client_secret: Optional[str] = None
    audience: Optional[str] = None
    default_redirect_uri: Optional[str] = None

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


class Auth0OIDCClient:
    def __init__(self, config: Optional[Auth0Config] = None, session: Optional[requests.Session] = None):
        self.config = config or load_auth0_config()
        self.session = session or requests.Session()

    def build_authorize_url(
        self,
        request: OAuthStartRequest,
        *,
        code_challenge: Optional[str] = None,
        code_challenge_method: Optional[str] = None,
        response_type: str = "code",
    ) -> str:
        params: Dict[str, Any] = {
            "response_type": response_type,
            "client_id": self.config.client_id,
            "redirect_uri": request.redirect_uri,
            "scope": normalize_scope(request.scope) or AUTH0_DEFAULT_SCOPE,
            "state": request.state or generate_state(),
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

    def exchange_code(self, request: CallbackRequest) -> TokenSet:
        payload: Dict[str, Any] = {
            "grant_type": "authorization_code",
            "client_id": self.config.client_id,
            "code": request.code,
            "redirect_uri": request.redirect_uri,
        }
        if self.config.client_secret:
            payload["client_secret"] = self.config.client_secret
        if request.code_verifier:
            payload["code_verifier"] = request.code_verifier
        response = self.session.post(self.config.token_url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return TokenSet(
            access_token=data["access_token"],
            id_token=data.get("id_token"),
            refresh_token=data.get("refresh_token"),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in"),
            scope=data.get("scope"),
            raw=data,
        )

    def fetch_userinfo(self, access_token: str) -> Dict[str, Any]:
        response = self.session.get(
            self.config.userinfo_url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


def load_auth0_config() -> Auth0Config:
    domain = os.environ["AUTH0_DOMAIN"]
    client_id = os.environ["AUTH0_CLIENT_ID"]
    return Auth0Config(
        domain=domain,
        client_id=client_id,
        client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
        audience=os.environ.get("AUTH0_AUDIENCE"),
        default_redirect_uri=os.environ.get("AUTH0_REDIRECT_URI"),
    )


def generate_state(length: int = 32) -> str:
    return secrets.token_urlsafe(length)


def generate_code_verifier(length: int = 64) -> str:
    verifier = secrets.token_urlsafe(length)
    return verifier[:128]


def generate_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
