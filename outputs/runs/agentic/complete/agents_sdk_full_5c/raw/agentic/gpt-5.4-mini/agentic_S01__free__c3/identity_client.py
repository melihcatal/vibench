from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class IdentityConfig:
    auth0_domain: str
    auth0_client_id: str
    auth0_client_secret: Optional[str]
    auth0_audience: Optional[str]
    auth0_connection: Optional[str]
    auth0_management_token: Optional[str]

    @property
    def base_url(self) -> str:
        return f"https://{self.auth0_domain}"


@lru_cache(maxsize=1)
def load_identity_config() -> IdentityConfig:
    return IdentityConfig(
        auth0_domain=os.environ["AUTH0_DOMAIN"],
        auth0_client_id=os.environ["AUTH0_CLIENT_ID"],
        auth0_client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
        auth0_audience=os.getenv("AUTH0_AUDIENCE"),
        auth0_connection=os.getenv("AUTH0_CONNECTION"),
        auth0_management_token=os.getenv("AUTH0_MANAGEMENT_TOKEN"),
    )


class Auth0Client:
    def __init__(self, config: IdentityConfig | None = None) -> None:
        self.config = config or load_identity_config()
        self.session = requests.Session()

    def token(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.config.base_url}/oauth/token",
            json=data,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def signup(self, email: str, password: str) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "client_id": self.config.auth0_client_id,
            "email": email,
            "password": password,
            "connection": self.config.auth0_connection or "Username-Password-Authentication",
        }
        response = self.session.post(
            f"{self.config.base_url}/dbconnections/signup",
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def password_change_ticket(self, email: str) -> Dict[str, Any]:
        if not self.config.auth0_management_token:
            raise RuntimeError("AUTH0_MANAGEMENT_TOKEN is required for password reset flow")
        response = self.session.post(
            f"{self.config.base_url}/api/v2/tickets/password-change",
            headers={"Authorization": f"Bearer {self.config.auth0_management_token}"},
            json={"email": email, "client_id": self.config.auth0_client_id},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
