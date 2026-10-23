from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


class Auth0Config:
    def __init__(self) -> None:
        self.domain = os.environ["AUTH0_DOMAIN"].rstrip("/")
        self.client_id = os.environ["AUTH0_CLIENT_ID"]
        self.client_secret = os.environ["AUTH0_CLIENT_SECRET"]
        self.management_audience = os.environ.get(
            "AUTH0_MANAGEMENT_AUDIENCE", f"https://{self.domain}/api/v2/"
        )
        self.default_audience = os.environ.get("AUTH0_AUDIENCE")
        self.connection = os.environ.get(
            "AUTH0_CONNECTION", "Username-Password-Authentication"
        )
        self.timeout = float(os.environ.get("AUTH0_TIMEOUT_SECONDS", "30"))

    @property
    def base_url(self) -> str:
        return f"https://{self.domain}"


class Auth0Client:
    def __init__(self, config: Optional[Auth0Config] = None) -> None:
        self.config = config or Auth0Config()
        self.session = requests.Session()

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.config.base_url}{path}",
            json=payload,
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return {}

    def _post_form(self, path: str, form: Dict[str, Any]) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.config.base_url}{path}",
            data=form,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        return response.json()

    def _management_access_token(self) -> str:
        token_data = self._post(
            "/oauth/token",
            {
                "grant_type": "client_credentials",
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
                "audience": self.config.management_audience,
            },
        )
        return token_data["access_token"]

    def create_database_user(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        management_token = self._management_access_token()
        response = self.session.post(
            f"{self.config.base_url}/api/v2/users",
            json=payload,
            headers={"Authorization": f"Bearer {management_token}"},
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        return response.json()

    def password_grant_login(
        self, username: str, password: str, scope: str, audience: Optional[str] = None
    ) -> Dict[str, Any]:
        form: Dict[str, Any] = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "scope": scope,
        }
        target_audience = audience or self.config.default_audience
        if target_audience:
            form["audience"] = target_audience
        return self._post_form("/oauth/token", form)

    def refresh_token(
        self, refresh_token: str, scope: Optional[str] = None
    ) -> Dict[str, Any]:
        form: Dict[str, Any] = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
        }
        if scope:
            form["scope"] = scope
        return self._post_form("/oauth/token", form)

    def start_password_reset(
        self, email: str, connection: Optional[str] = None
    ) -> Dict[str, Any]:
        return self._post(
            "/dbconnections/change_password",
            {
                "client_id": self.config.client_id,
                "email": email,
                "connection": connection or self.config.connection,
            },
        )
