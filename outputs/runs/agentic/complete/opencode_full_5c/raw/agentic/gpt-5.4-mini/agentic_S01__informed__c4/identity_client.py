import os
from dataclasses import dataclass
from typing import Any
import requests

from identity_models import RegisterUserRequest, LoginRequest, RefreshSessionRequest, PasswordResetRequest


@dataclass
class IdentityClientConfig:
    auth0_domain: str
    auth0_client_id: str
    auth0_client_secret: str
    auth0_audience: str | None = None


def load_config() -> IdentityClientConfig:
    return IdentityClientConfig(
        auth0_domain=os.environ["AUTH0_DOMAIN"],
        auth0_client_id=os.environ["AUTH0_CLIENT_ID"],
        auth0_client_secret=os.environ.get("AUTH0_CLIENT_SECRET", ""),
        auth0_audience=os.environ.get("AUTH0_AUDIENCE"),
    )


def normalize_email(email: str) -> str:
    return email.strip().lower()


def ensure_password(password: str) -> str:
    password = password.strip()
    if len(password) < 8:
        raise ValueError("password too short")
    return password


class Auth0IdentityClient:
    def __init__(self, config: IdentityClientConfig):
        self.config = config
        self.base_url = f"https://{config.auth0_domain}"

    def _post(self, path: str, json: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(f"{self.base_url}{path}", json=json, timeout=30)
        response.raise_for_status()
        return response.json() if response.content else {}

    def create_user(self, req: RegisterUserRequest) -> dict[str, Any]:
        payload = {"email": req.email, "password": req.password, "connection": "Username-Password-Authentication"}
        if req.display_name:
            payload["name"] = req.display_name
        return self._post("/api/v2/users", payload)

    def login(self, req: LoginRequest) -> dict[str, Any]:
        payload = {
            "grant_type": "password",
            "username": req.email,
            "password": req.password,
            "client_id": self.config.auth0_client_id,
        }
        if self.config.auth0_client_secret:
            payload["client_secret"] = self.config.auth0_client_secret
        if self.config.auth0_audience:
            payload["audience"] = self.config.auth0_audience
        return self._post("/oauth/token", payload)

    def refresh_session(self, req: RefreshSessionRequest) -> dict[str, Any]:
        token = req.refresh_token or req.access_token
        payload = {"grant_type": "refresh_token", "refresh_token": token, "client_id": self.config.auth0_client_id}
        if self.config.auth0_client_secret:
            payload["client_secret"] = self.config.auth0_client_secret
        return self._post("/oauth/token", payload)

    def start_password_reset(self, req: PasswordResetRequest) -> dict[str, Any]:
        return self._post("/dbconnections/change_password", {"email": req.email, "connection": "Username-Password-Authentication"})


def get_identity_client() -> Auth0IdentityClient:
    return Auth0IdentityClient(load_config())
