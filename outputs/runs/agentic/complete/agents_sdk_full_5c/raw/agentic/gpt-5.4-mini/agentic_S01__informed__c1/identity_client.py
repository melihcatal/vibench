from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests
from auth0.management import Auth0

from identity_models import (
    ActionResult,
    IdentityTokens,
    LoginRequest,
    PasswordResetRequest,
    RefreshRequest,
    RegisterUserRequest,
)


class IdentityConfig:
    def __init__(self) -> None:
        self.domain = os.getenv("AUTH0_DOMAIN", "")
        self.client_id = os.getenv("AUTH0_CLIENT_ID", "")
        self.client_secret = os.getenv("AUTH0_CLIENT_SECRET", "")
        self.audience = os.getenv("AUTH0_AUDIENCE", "")
        self.connection = os.getenv("AUTH0_DB_CONNECTION", "Username-Password-Authentication")
        self.management_token = os.getenv("AUTH0_MANAGEMENT_TOKEN", "")
        self.base_url = f"https://{self.domain}" if self.domain else ""


class IdentityClient:
    def __init__(self, config: Optional[IdentityConfig] = None) -> None:
        self.config = config or IdentityConfig()
        self._auth0 = Auth0(self.config.domain, self.config.management_token) if self.config.domain and self.config.management_token else None

    def register_user(self, request: RegisterUserRequest) -> Dict[str, Any]:
        req = request.normalized()
        if self._auth0 is not None:
            return self._auth0.users.create({
                "email": req.email,
                "password": req.password,
                "connection": self.config.connection,
                "name": req.display_name,
                "email_verified": False,
            })
        resp = requests.post(
            f"{self.config.base_url}/dbconnections/signup",
            json={
                "client_id": self.config.client_id,
                "email": req.email,
                "password": req.password,
                "connection": self.config.connection,
                "username": req.display_name,
            },
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def login(self, request: LoginRequest) -> IdentityTokens:
        req = request.normalized()
        resp = requests.post(
            f"{self.config.base_url}/oauth/token",
            json={
                "grant_type": "password",
                "username": req.email,
                "password": req.password,
                "audience": self.config.audience or None,
                "scope": "openid profile email offline_access",
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return IdentityTokens(
            access_token=data.get("access_token", ""),
            id_token=data.get("id_token"),
            refresh_token=data.get("refresh_token"),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in"),
            raw=data,
        )

    def refresh(self, request: RefreshRequest) -> IdentityTokens:
        resp = requests.post(
            f"{self.config.base_url}/oauth/token",
            json={
                "grant_type": "refresh_token",
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
                "refresh_token": request.refresh_token,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return IdentityTokens(
            access_token=data.get("access_token", ""),
            id_token=data.get("id_token"),
            refresh_token=data.get("refresh_token", request.refresh_token),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in"),
            raw=data,
        )

    def password_reset(self, request: PasswordResetRequest) -> ActionResult:
        req = request.normalized()
        resp = requests.post(
            f"{self.config.base_url}/dbconnections/change_password",
            json={
                "client_id": self.config.client_id,
                "email": req.email,
                "connection": self.config.connection,
            },
            timeout=30,
        )
        resp.raise_for_status()
        return ActionResult(ok=True, message=resp.text.strip(), raw={"status_code": resp.status_code})
