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
        management_client_id: Optional[str] = None,
        management_client_secret: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        self.domain = (domain or os.environ["AUTH0_DOMAIN"]).strip()
        self.client_id = client_id or os.environ["AUTH0_CLIENT_ID"]
        self.client_secret = client_secret or os.getenv("AUTH0_CLIENT_SECRET")
        self.management_client_id = management_client_id or os.getenv("AUTH0_MANAGEMENT_CLIENT_ID", self.client_id)
        self.management_client_secret = management_client_secret or os.getenv("AUTH0_MANAGEMENT_CLIENT_SECRET", self.client_secret)
        self.timeout = timeout
        self.base_url = f"https://{self.domain}"
        self.session = requests.Session()

    def _post(self, path: str, json_body: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}{path}",
            json=json_body,
            headers=headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return {}

    def get_management_token(self) -> str:
        if not self.management_client_secret:
            raise ValueError("AUTH0_MANAGEMENT_CLIENT_SECRET or AUTH0_CLIENT_SECRET is required for Auth0 Management API")
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.management_client_id,
            "client_secret": self.management_client_secret,
            "audience": f"https://{self.domain}/api/v2/",
        }
        data = self._post("/oauth/token", payload)
        return data["access_token"]

    def management_headers(self) -> Dict[str, str]:
        token = self.get_management_token()
        return {"Authorization": f"Bearer {token}"}

    def create_database_user(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/api/v2/users", payload, headers=self.management_headers())

    def password_grant_login(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/oauth/token", payload)

    def refresh_token_grant(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/oauth/token", payload)

    def start_password_reset(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/dbconnections/change_password", payload)
