from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


class IdentityConfigError(RuntimeError):
    pass


class Auth0IdentityClient:
    def __init__(self) -> None:
        self.domain = self._require_env("AUTH0_DOMAIN")
        self.client_id = self._require_env("AUTH0_CLIENT_ID")
        self.client_secret = self._require_env("AUTH0_CLIENT_SECRET")
        self.connection = os.getenv("AUTH0_DB_CONNECTION", "Username-Password-Authentication")
        self.audience = os.getenv("AUTH0_AUDIENCE")
        self.timeout = float(os.getenv("AUTH0_TIMEOUT_SECONDS", "20"))
        self.base_url = f"https://{self.domain}"

    def _require_env(self, name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise IdentityConfigError(f"Missing required environment variable: {name}")
        return value

    def endpoint(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def post_json(
        self,
        path: str,
        payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        merged_headers = {"content-type": "application/json"}
        if headers:
            merged_headers.update(headers)
        response = requests.post(
            self.endpoint(path),
            json=payload,
            headers=merged_headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        if not response.content:
            return {}
        return response.json()


def get_identity_client() -> Auth0IdentityClient:
    return Auth0IdentityClient()
