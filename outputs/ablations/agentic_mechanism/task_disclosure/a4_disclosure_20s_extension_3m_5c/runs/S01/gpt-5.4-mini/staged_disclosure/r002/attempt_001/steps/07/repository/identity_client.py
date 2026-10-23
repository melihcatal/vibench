import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class IdentityConfig:
    auth0_domain: str = os.getenv("AUTH0_DOMAIN", "")
    auth0_client_id: str = os.getenv("AUTH0_CLIENT_ID", "")
    auth0_client_secret: str = os.getenv("AUTH0_CLIENT_SECRET", "")
    auth0_audience: str = os.getenv("AUTH0_AUDIENCE", "")
    auth0_connection: str = os.getenv("AUTH0_CONNECTION", "Username-Password-Authentication")
    auth0_management_token: str = os.getenv("AUTH0_MANAGEMENT_TOKEN", "")


class Auth0IdentityClient:
    def __init__(self, config: Optional[IdentityConfig] = None) -> None:
        self.config = config or IdentityConfig()
        self.session = requests.Session()
        self.base_url = f"https://{self.config.auth0_domain}" if self.config.auth0_domain else ""

    def _require(self, value: str, name: str) -> str:
        if not value:
            raise ValueError(f"Missing required configuration: {name}")
        return value

    def _post(self, path: str, json: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = self.session.post(url, json=json, headers=headers or {}, timeout=30)
        response.raise_for_status()
        return response.json() if response.content else {}

    def _delete(self, path: str, headers: Optional[Dict[str, str]] = None) -> None:
        url = f"{self.base_url}{path}"
        response = self.session.delete(url, headers=headers or {}, timeout=30)
        response.raise_for_status()

    def _management_headers(self) -> Dict[str, str]:
        token = self._require(self.config.auth0_management_token, "AUTH0_MANAGEMENT_TOKEN")
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def _password_grant_headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/json"}

    def create_account(self, email: str, password: str, user_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self._require(self.config.auth0_domain, "AUTH0_DOMAIN")
        return self._post(
            "/api/v2/users",
            {
                "email": email,
                "password": password,
                "connection": self._require(self.config.auth0_connection, "AUTH0_CONNECTION"),
                "user_metadata": user_metadata or {},
            },
            headers=self._management_headers(),
        )

    def login(self, email: str, password: str) -> Dict[str, Any]:
        self._require(self.config.auth0_domain, "AUTH0_DOMAIN")
        return self._post(
            "/oauth/token",
            {
                "grant_type": "password",
                "username": email,
                "password": password,
                "audience": self._require(self.config.auth0_audience, "AUTH0_AUDIENCE"),
                "client_id": self._require(self.config.auth0_client_id, "AUTH0_CLIENT_ID"),
                "client_secret": self._require(self.config.auth0_client_secret, "AUTH0_CLIENT_SECRET"),
                "scope": "openid profile email offline_access",
            },
            headers=self._password_grant_headers(),
        )

    def change_password(self, email: str) -> Dict[str, Any]:
        self._require(self.config.auth0_domain, "AUTH0_DOMAIN")
        return self._post(
            "/dbconnections/change_password",
            {
                "client_id": self._require(self.config.auth0_client_id, "AUTH0_CLIENT_ID"),
                "email": email,
                "connection": self._require(self.config.auth0_connection, "AUTH0_CONNECTION"),
            },
            headers=self._password_grant_headers(),
        )

    def delete_account(self, user_id: str) -> None:
        self._require(self.config.auth0_domain, "AUTH0_DOMAIN")
        self._delete(f"/api/v2/users/{user_id}", headers=self._management_headers())


def get_identity_client() -> Auth0IdentityClient:
    return Auth0IdentityClient()
