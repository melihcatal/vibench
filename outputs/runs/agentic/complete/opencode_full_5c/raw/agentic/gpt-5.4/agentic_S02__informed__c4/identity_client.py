from __future__ import annotations

import base64
import hashlib
import os
import secrets
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests


class Auth0OIDCClient:
    def __init__(self) -> None:
        self.domain = os.environ["AUTH0_DOMAIN"]
        self.client_id = os.environ["AUTH0_CLIENT_ID"]
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.default_audience = os.environ.get("AUTH0_AUDIENCE")
        self.timeout = float(os.environ.get("AUTH0_HTTP_TIMEOUT", "15"))

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

    def build_authorize_url(
        self,
        *,
        redirect_uri: str,
        state: str,
        scope: str,
        audience: Optional[str] = None,
        prompt: Optional[str] = None,
        connection: Optional[str] = None,
        login_hint: Optional[str] = None,
        code_challenge: Optional[str] = None,
        code_challenge_method: Optional[str] = None,
    ) -> str:
        params: Dict[str, Any] = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "state": state,
        }
        resolved_audience = audience or self.default_audience
        if resolved_audience:
            params["audience"] = resolved_audience
        if prompt:
            params["prompt"] = prompt
        if connection:
            params["connection"] = connection
        if login_hint:
            params["login_hint"] = login_hint
        if code_challenge:
            params["code_challenge"] = code_challenge
        if code_challenge_method:
            params["code_challenge_method"] = code_challenge_method
        return f"{self.authorize_url}?{urlencode(params)}"

    def exchange_code(
        self,
        *,
        code: str,
        redirect_uri: str,
        code_verifier: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "code": code,
            "redirect_uri": redirect_uri,
        }
        if self.client_secret:
            payload["client_secret"] = self.client_secret
        if code_verifier:
            payload["code_verifier"] = code_verifier
        response = requests.post(self.token_url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def fetch_userinfo(self, access_token: str) -> Dict[str, Any]:
        response = requests.get(
            self.userinfo_url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()


def generate_pkce_verifier(length: int = 64) -> str:
    raw = secrets.token_urlsafe(length)
    return raw[:128]


def generate_pkce_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
