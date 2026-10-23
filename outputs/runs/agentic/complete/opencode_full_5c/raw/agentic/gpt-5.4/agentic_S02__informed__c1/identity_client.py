from __future__ import annotations

import os
import secrets
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from identity_models import compact_dict, normalize_scope


class Auth0OIDCClient:
    def __init__(self) -> None:
        self.domain = os.environ["AUTH0_DOMAIN"]
        self.client_id = os.environ["AUTH0_CLIENT_ID"]
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.default_audience = os.environ.get("AUTH0_AUDIENCE")
        self.base_url = f"https://{self.domain}"
        self.authorization_endpoint = f"{self.base_url}/authorize"
        self.token_endpoint = f"{self.base_url}/oauth/token"
        self.userinfo_endpoint = f"{self.base_url}/userinfo"

    def new_state(self) -> str:
        return secrets.token_urlsafe(24)

    def build_authorization_url(
        self,
        redirect_uri: str,
        scope: Optional[str] = None,
        state: Optional[str] = None,
        audience: Optional[str] = None,
        prompt: Optional[str] = None,
        connection: Optional[str] = None,
        code_challenge: Optional[str] = None,
        code_challenge_method: Optional[str] = None,
    ) -> str:
        query = compact_dict(
            {
                "response_type": "code",
                "client_id": self.client_id,
                "redirect_uri": redirect_uri,
                "scope": normalize_scope(scope),
                "state": state or self.new_state(),
                "audience": audience or self.default_audience,
                "prompt": prompt,
                "connection": connection,
                "code_challenge": code_challenge,
                "code_challenge_method": code_challenge_method,
            }
        )
        return f"{self.authorization_endpoint}?{urlencode(query)}"

    def exchange_code(
        self,
        code: str,
        redirect_uri: str,
        code_verifier: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = compact_dict(
            {
                "grant_type": "authorization_code",
                "client_id": self.client_id,
                "client_secret": self.client_secret if code_verifier is None else None,
                "code": code,
                "redirect_uri": redirect_uri,
                "code_verifier": code_verifier,
            }
        )
        response = requests.post(
            self.token_endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def fetch_userinfo(self, access_token: str) -> Dict[str, Any]:
        response = requests.get(
            self.userinfo_endpoint,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
