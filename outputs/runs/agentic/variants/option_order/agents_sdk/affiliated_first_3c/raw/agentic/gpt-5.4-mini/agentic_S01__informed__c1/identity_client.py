from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

from identity_models import AuthTokens, IdentityUser

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "")
AUTH0_CONNECTION = os.getenv("AUTH0_CONNECTION", "Username-Password-Authentication")


@dataclass
class Auth0ClientConfig:
    domain: str
    client_id: str
    client_secret: str
    audience: str = ""
    connection: str = "Username-Password-Authentication"

    @classmethod
    def from_env(cls) -> "Auth0ClientConfig":
        return cls(
            domain=AUTH0_DOMAIN,
            client_id=AUTH0_CLIENT_ID,
            client_secret=AUTH0_CLIENT_SECRET,
            audience=AUTH0_AUDIENCE,
            connection=AUTH0_CONNECTION,
        )


class Auth0IdentityClient:
    def __init__(self, config: Optional[Auth0ClientConfig] = None, session: Optional[requests.Session] = None):
        self.config = config or Auth0ClientConfig.from_env()
        self.session = session or requests.Session()
        if not self.config.domain or not self.config.client_id:
            raise ValueError("AUTH0_DOMAIN and AUTH0_CLIENT_ID are required")

    @property
    def base_url(self) -> str:
        return f"https://{self.config.domain}"

    def token_endpoint(self) -> str:
        return f"{self.base_url}/oauth/token"

    def management_headers(self, token: str) -> Dict[str, str]:
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def password_realm_grant(self, email: str, password: str) -> AuthTokens:
        payload: Dict[str, Any] = {
            "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
            "username": email,
            "password": password,
            "realm": self.config.connection,
            "client_id": self.config.client_id,
        }
        if self.config.client_secret:
            payload["client_secret"] = self.config.client_secret
        if self.config.audience:
            payload["audience"] = self.config.audience
        response = self.session.post(self.token_endpoint(), json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return AuthTokens(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
            expires_in=data.get("expires_in"),
            raw=data,
        )

    def refresh(self, refresh_token: str) -> AuthTokens:
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.config.client_id,
            "refresh_token": refresh_token,
        }
        if self.config.client_secret:
            payload["client_secret"] = self.config.client_secret
        response = self.session.post(self.token_endpoint(), json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return AuthTokens(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token", refresh_token),
            id_token=data.get("id_token"),
            expires_in=data.get("expires_in"),
            raw=data,
        )

    def create_user(self, email: str, password: str, display_name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> IdentityUser:
        payload: Dict[str, Any] = {
            "email": email,
            "password": password,
            "connection": self.config.connection,
            "email_verified": False,
        }
        if display_name:
            payload["name"] = display_name
        if metadata:
            payload["user_metadata"] = metadata
        response = self.session.post(f"{self.base_url}/api/v2/users", json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return IdentityUser(
            user_id=data["user_id"],
            email=data.get("email", email),
            email_verified=data.get("email_verified", False),
            display_name=data.get("name"),
            raw=data,
        )

    def start_password_reset(self, email: str) -> Dict[str, Any]:
        payload = {"client_id": self.config.client_id, "email": email, "connection": self.config.connection}
        response = self.session.post(f"{self.base_url}/dbconnections/change_password", json=payload, timeout=30)
        response.raise_for_status()
        return {"message": response.text.strip(), "status_code": response.status_code}

    def get_user(self, user_id: str, management_token: str) -> IdentityUser:
        response = self.session.get(f"{self.base_url}/api/v2/users/{user_id}", headers=self.management_headers(management_token), timeout=30)
        response.raise_for_status()
        data = response.json()
        return IdentityUser(
            user_id=data["user_id"],
            email=data.get("email", ""),
            email_verified=data.get("email_verified", False),
            display_name=data.get("name"),
            raw=data,
        )
