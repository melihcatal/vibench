from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

from identity_models import IdentityResult

AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_CONNECTION_ENV = "AUTH0_CONNECTION"


class IdentityClient:
    def __init__(self, domain: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None, connection: Optional[str] = None):
        self.domain = domain or os.getenv(AUTH0_DOMAIN_ENV, "")
        self.client_id = client_id or os.getenv(AUTH0_CLIENT_ID_ENV, "")
        self.client_secret = client_secret or os.getenv(AUTH0_CLIENT_SECRET_ENV, "")
        self.connection = connection or os.getenv(AUTH0_CONNECTION_ENV, "Username-Password-Authentication")
        self.base_url = f"https://{self.domain}" if self.domain else ""

    def headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/json"}

    def auth0_request(self, method: str, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self.base_url:
            raise ValueError("AUTH0_DOMAIN is required for Auth0 Management API calls")
        url = f"{self.base_url}{path}"
        response = requests.request(method, url, headers=self.headers(), json=json, timeout=30)
        response.raise_for_status()
        if response.text:
            return response.json()
        return {}

    def result(self, success: bool, data: Dict[str, Any], error: Optional[str] = None) -> IdentityResult:
        return IdentityResult(success=success, provider="Auth0 Management API", data=data, error=error)


def get_identity_client() -> IdentityClient:
    return IdentityClient()
