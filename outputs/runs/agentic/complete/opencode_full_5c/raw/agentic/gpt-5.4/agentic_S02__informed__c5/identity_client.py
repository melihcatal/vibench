from __future__ import annotations

import base64
import hashlib
import os
import secrets
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from identity_models import OAuthState, TokenSet


class Auth0OIDCClient:
    def __init__(self) -> None:
        self.domain = os.environ["AUTH0_DOMAIN"].rstrip("/")
        self.client_id = os.environ["AUTH0_CLIENT_ID"]
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.audience = os.environ.get("AUTH0_AUDIENCE")
        self.default_scope = os.environ.get(
            "AUTH0_SCOPE", "openid profile email offline_access"
        )
        self.base_url = f"https://{self.domain}"
        self.authorize_url = f"{self.base_url}/authorize"
        self.token_url = f"{self.base_url}/oauth/token"
        self.userinfo_url = f"{self.base_url}/userinfo"

    def create_state(
        self, redirect_uri: str, code_verifier: Optional[str] = None
    ) -> OAuthState:
        return OAuthState(
            state=secrets.token_urlsafe(32),
            redirect_uri=redirect_uri,
            code_verifier=code_verifier,
            nonce=secrets.token_urlsafe(24),
            provider="auth0",
        )

    def build_authorization_url(
        self,
        oauth_state: OAuthState,
        scope: Optional[str] = None,
        use_pkce: bool = False,
    ) -> str:
        params: Dict[str, Any] = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": oauth_state.redirect_uri,
            "scope": scope or self.default_scope,
            "state": oauth_state.state,
            "nonce": oauth_state.nonce,
        }
        if self.audience:
            params["audience"] = self.audience
        if use_pkce and oauth_state.code_verifier:
            params["code_challenge"] = pkce_challenge(oauth_state.code_verifier)
            params["code_challenge_method"] = "S256"
        return f"{self.authorize_url}?{urlencode(params)}"

    def exchange_code(
        self, code: str, redirect_uri: str, code_verifier: Optional[str] = None
    ) -> TokenSet:
        payload: Dict[str, Any] = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "code": code,
            "redirect_uri": redirect_uri,
        }
        if code_verifier:
            payload["code_verifier"] = code_verifier
        elif self.client_secret:
            payload["client_secret"] = self.client_secret
        elif self.client_secret:
            payload["client_secret"] = self.client_secret
        response = requests.post(self.token_url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return TokenSet(
            access_token=data["access_token"],
            id_token=data.get("id_token"),
            refresh_token=data.get("refresh_token"),
            token_type=data.get("token_type", "Bearer"),
            expires_in=int(data.get("expires_in", 0)),
            scope=data.get("scope"),
            raw=data,
        )

    def fetch_userinfo(self, access_token: str) -> Dict[str, Any]:
        response = requests.get(
            self.userinfo_url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


def generate_code_verifier(length: int = 64) -> str:
    raw = secrets.token_urlsafe(length)
    return raw[:128]


def pkce_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
