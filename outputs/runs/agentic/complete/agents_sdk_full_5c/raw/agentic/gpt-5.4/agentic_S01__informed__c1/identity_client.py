from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


class Auth0Client:
    def __init__(
        self,
        domain: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        audience: Optional[str] = None,
        connection: Optional[str] = None,
        management_audience: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        self.domain = domain or os.environ["AUTH0_DOMAIN"]
        self.client_id = client_id or os.environ["AUTH0_CLIENT_ID"]
        self.client_secret = client_secret or os.environ["AUTH0_CLIENT_SECRET"]
        self.audience = audience or os.getenv("AUTH0_AUDIENCE")
        self.connection = connection or os.getenv("AUTH0_CONNECTION", "Username-Password-Authentication")
        self.management_audience = management_audience or os.getenv(
            "AUTH0_MANAGEMENT_AUDIENCE", f"https://{self.domain}/api/v2/"
        )
        self.timeout = timeout
        self.base_url = f"https://{self.domain}"

    def _post(self, path: str, json_body: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}{path}",
            json=json_body,
            timeout=self.timeout,
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return {}

    def get_management_token(self) -> str:
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.management_audience,
        }
        data = self._post("/oauth/token", payload)
        return data["access_token"]

    def management_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.get_management_token()}",
            "Content-Type": "application/json",
        }

    def management_post(self, path: str, json_body: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}{path}",
            headers=self.management_headers(),
            json=json_body,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()


def get_auth0_client() -> Auth0Client:
    return Auth0Client()
