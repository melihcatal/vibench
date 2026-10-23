from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional

import requests

from identity_models import AuthTokens, ResetFlowResult, compact_mapping

AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"
AUTH0_CONNECTION_ENV = "AUTH0_DB_CONNECTION"


@dataclass(slots=True)
class IdentityClientConfig:
    domain: str
    client_id: str
    client_secret: Optional[str] = None
    audience: Optional[str] = None
    connection: str = "Username-Password-Authentication"

    @classmethod
    def from_env(cls) -> "IdentityClientConfig":
        return cls(
            domain=os.environ.get(AUTH0_DOMAIN_ENV, ""),
            client_id=os.environ.get(AUTH0_CLIENT_ID_ENV, ""),
            client_secret=os.environ.get(AUTH0_CLIENT_SECRET_ENV),
            audience=os.environ.get(AUTH0_AUDIENCE_ENV),
            connection=os.environ.get(AUTH0_CONNECTION_ENV, "Username-Password-Authentication"),
        )


class Auth0IdentityClient:
    def __init__(self, config: Optional[IdentityClientConfig] = None, session: Optional[requests.Session] = None) -> None:
        self.config = config or IdentityClientConfig.from_env()
        self.session = session or requests.Session()

    @property
    def token_url(self) -> str:
        return f"https://{self.config.domain}/oauth/token"

    @property
    def users_url(self) -> str:
        return f"https://{self.config.domain}/api/v2/users"

    @property
    def password_change_url(self) -> str:
        return f"https://{self.config.domain}/dbconnections/change_password"

    def register_user(self, email: str, password: str, name: Optional[str] = None, metadata: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        payload = {
            "client_id": self.config.client_id,
            "email": email,
            "password": password,
            "connection": self.config.connection,
            "name": name,
            "user_metadata": compact_mapping(metadata),
        }
        response = self.session.post(self.users_url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def login_password(self, email: str, password: str) -> AuthTokens:
        payload = {
            "grant_type": "password",
            "username": email,
            "password": password,
            "audience": self.config.audience,
            "scope": "openid profile email offline_access",
            "client_id": self.config.client_id,
        }
        if self.config.client_secret:
            payload["client_secret"] = self.config.client_secret
        response = self.session.post(self.token_url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return AuthTokens(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in"),
            raw=data,
        )

    def refresh_session(self, refresh_token: str) -> AuthTokens:
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.config.client_id,
        }
        if self.config.client_secret:
            payload["client_secret"] = self.config.client_secret
        response = self.session.post(self.token_url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return AuthTokens(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token", refresh_token),
            id_token=data.get("id_token"),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in"),
            raw=data,
        )

    def start_password_reset(self, email: str) -> ResetFlowResult:
        payload = {
            "client_id": self.config.client_id,
            "email": email,
            "connection": self.config.connection,
        }
        response = self.session.post(self.password_change_url, json=payload, timeout=30)
        response.raise_for_status()
        return ResetFlowResult(success=True, message=response.text.strip() or "Password reset initiated", raw={"status_code": response.status_code})
