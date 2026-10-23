from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True, slots=True)
class Auth0Settings:
    domain: str
    client_id: str
    client_secret: str
    audience: Optional[str] = None
    management_audience: str = "https://{domain}/api/v2/"

    @property
    def base_url(self) -> str:
        return f"https://{self.domain}"

    @property
    def management_api_audience(self) -> str:
        return self.management_audience.format(domain=self.domain)


class Auth0Client:
    def __init__(self, settings: Optional[Auth0Settings] = None, timeout: int = 30) -> None:
        self.settings = settings or load_auth0_settings()
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self.session.post(f"{self.settings.base_url}{path}", json=payload, timeout=self.timeout)
        response.raise_for_status()
        if response.content:
            return response.json()
        return {}

    def create_db_user(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.post("/dbconnections/signup", payload)

    def password_grant_login(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.post("/oauth/token", payload)

    def refresh_token(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.post("/oauth/token", payload)

    def start_password_reset(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.post("/dbconnections/change_password", payload)


def load_auth0_settings() -> Auth0Settings:
    return Auth0Settings(
        domain=os.environ["AUTH0_DOMAIN"],
        client_id=os.environ["AUTH0_CLIENT_ID"],
        client_secret=os.environ["AUTH0_CLIENT_SECRET"],
        audience=os.getenv("AUTH0_AUDIENCE"),
    )
