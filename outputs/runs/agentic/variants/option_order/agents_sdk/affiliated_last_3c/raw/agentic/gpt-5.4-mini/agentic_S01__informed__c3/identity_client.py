from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any, Dict, Optional

import requests

from identity_models import (
    IdentityResult,
    LoginRequest,
    PasswordResetRequest,
    RefreshRequest,
    RegisterUserRequest,
    Tokens,
)

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_CONNECTION = os.getenv("AUTH0_CONNECTION", "Username-Password-Authentication")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "")
AUTH0_MANAGEMENT_AUDIENCE = os.getenv("AUTH0_MANAGEMENT_AUDIENCE", f"https://{AUTH0_DOMAIN}/api/v2/") if AUTH0_DOMAIN else ""


def auth0_base_url() -> str:
    if not AUTH0_DOMAIN:
        raise RuntimeError("AUTH0_DOMAIN is required")
    return f"https://{AUTH0_DOMAIN}"


class Auth0IdentityClient:
    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self.session = session or requests.Session()

    def _oauth_token(self) -> str:
        url = f"{auth0_base_url()}/oauth/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": AUTH0_CLIENT_ID,
            "client_secret": AUTH0_CLIENT_SECRET,
            "audience": AUTH0_MANAGEMENT_AUDIENCE,
        }
        response = self.session.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["access_token"]

    def _management_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self._oauth_token()}", "Content-Type": "application/json"}

    def register_user(self, req: RegisterUserRequest) -> IdentityResult:
        r = req.normalized()
        payload: Dict[str, Any] = {
            "connection": AUTH0_CONNECTION,
            "email": r.email,
            "password": r.password,
            "user_metadata": {"display_name": r.display_name, "locale": r.locale},
        }
        response = self.session.post(f"{auth0_base_url()}/api/v2/users", headers=self._management_headers(), json=payload, timeout=30)
        if response.ok:
            return IdentityResult(True, "Auth0", response.json())
        return IdentityResult(False, "Auth0", {}, response.text)

    def login(self, req: LoginRequest) -> Tokens:
        r = req.normalized()
        payload = {
            "grant_type": "password",
            "username": r.email,
            "password": r.password,
            "audience": AUTH0_AUDIENCE or AUTH0_MANAGEMENT_AUDIENCE,
            "scope": "openid profile email offline_access",
            "client_id": AUTH0_CLIENT_ID,
            "client_secret": AUTH0_CLIENT_SECRET,
        }
        response = self.session.post(f"{auth0_base_url()}/oauth/token", json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return Tokens(data.get("access_token", ""), data.get("refresh_token"), data.get("id_token"), data.get("expires_in"), data)

    def refresh(self, req: RefreshRequest) -> Tokens:
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": req.refresh_token,
            "client_id": AUTH0_CLIENT_ID,
            "client_secret": AUTH0_CLIENT_SECRET,
        }
        response = self.session.post(f"{auth0_base_url()}/oauth/token", json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return Tokens(data.get("access_token", ""), data.get("refresh_token"), data.get("id_token"), data.get("expires_in"), data)

    def start_password_reset(self, req: PasswordResetRequest) -> IdentityResult:
        r = req.normalized()
        payload = {"client_id": AUTH0_CLIENT_ID, "email": r.email, "connection": AUTH0_CONNECTION}
        response = self.session.post(f"{auth0_base_url()}/dbconnections/change_password", json=payload, timeout=30)
        if response.ok:
            return IdentityResult(True, "Auth0", {"message": response.text})
        return IdentityResult(False, "Auth0", {}, response.text)
