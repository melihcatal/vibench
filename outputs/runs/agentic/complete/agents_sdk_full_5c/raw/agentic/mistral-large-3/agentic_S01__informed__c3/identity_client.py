import os
import requests
from typing import Optional, Dict, Any
from identity_models import (
    RegisterUserRequest,
    RegisterUserResponse,
    LoginRequest,
    LoginResponse,
    RefreshSessionRequest,
    RefreshSessionResponse,
    PasswordResetRequest,
    PasswordResetResponse,
    Auth0User,
    Auth0TokenResponse,
)


class Auth0Client:
    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN")
        self.client_id = os.getenv("AUTH0_CLIENT_ID")
        self.client_secret = os.getenv("AUTH0_CLIENT_SECRET")
        self.audience = f"https://{self.domain}/api/v2/"
        self.connection = "Username-Password-Authentication"

    def _get_management_token(self) -> str:
        url = f"https://{self.domain}/oauth/token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.audience,
            "grant_type": "client_credentials",
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["access_token"]

    def _normalize_register_response(self, response: Dict[str, Any]) -> RegisterUserResponse:
        return {
            "user_id": response["_id"],
            "email_verified": response.get("email_verified", False),
            "status": "created",
        }

    def _normalize_login_response(self, response: Dict[str, Any]) -> LoginResponse:
        return {
            "access_token": response["access_token"],
            "refresh_token": response.get("refresh_token", ""),
            "expires_in": response["expires_in"],
            "id_token": response.get("id_token"),
        }

    def _normalize_refresh_response(self, response: Dict[str, Any]) -> RefreshSessionResponse:
        return {
            "access_token": response["access_token"],
            "expires_in": response["expires_in"],
            "id_token": response.get("id_token"),
        }

    def _normalize_password_reset_response(self, status: str) -> PasswordResetResponse:
        return {
            "status": status,
            "reset_sent": True,
        }