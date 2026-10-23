import os
import requests
from typing import Dict, Any
from identity_models import (
    RegisterUserRequest,
    RegisterUserResponse,
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    PasswordResetRequest,
    PasswordResetResponse,
)


class Auth0Client:
    def __init__(self):
        self.domain = os.environ.get("AUTH0_DOMAIN")
        self.client_id = os.environ.get("AUTH0_CLIENT_ID")
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.audience = os.environ.get("AUTH0_AUDIENCE")
        if not all([self.domain, self.client_id, self.client_secret, self.audience]):
            raise ValueError(
                "AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, and AUTH0_AUDIENCE must be set in environment variables"
            )

        self.management_api_url = f"https://{self.domain}/api/v2/"
        self.auth_api_url = f"https://{self.domain}/oauth/token"

        # Obtain Management API Token (for user registration, password reset, etc.)
        self._management_token = self._get_management_api_token()

    def _get_management_api_token(self) -> str:
        headers = {"content-type": "application/json"}
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.management_api_url,
            "grant_type": "client_credentials",
        }
        try:
            res = requests.post(self.auth_api_url, json=payload, headers=headers)
            res.raise_for_status()
            return res.json()["access_token"]
        except requests.exceptions.RequestException as e:
            print(f"Error obtaining management API token: {e}")
            raise

    def _get_auth_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self._management_token}",
            "Content-Type": "application/json",
        }

    def register_user(self, request: RegisterUserRequest) -> RegisterUserResponse:
        url = f"{self.management_api_url}users"
        payload = {
            "email": request.email,
            "password": request.password,
            "connection": request.connection,
        }
        try:
            res = requests.post(url, json=payload, headers=self._get_auth_headers())
            res.raise_for_status()
            return RegisterUserResponse(**res.json())
        except requests.exceptions.RequestException as e:
            print(f"Error registering user: {e}")
            raise

    def login_user(self, request: LoginRequest) -> LoginResponse:
        url = self.auth_api_url
        payload = {
            "grant_type": request.grant_type,
            "client_id": request.client_id,
            "username": request.username,
            "password": request.password,
            "audience": request.audience,
            "scope": request.scope,
        }
        try:
            res = requests.post(url, json=payload)
            res.raise_for_status()
            return LoginResponse(**res.json())
        except requests.exceptions.RequestException as e:
            print(f"Error logging in user: {e}")
            raise

    def refresh_access_token(
        self, request: RefreshTokenRequest
    ) -> RefreshTokenResponse:
        url = self.auth_api_url
        payload = {
            "grant_type": request.grant_type,
            "client_id": request.client_id,
            "refresh_token": request.refresh_token,
        }
        try:
            res = requests.post(url, json=payload)
            res.raise_for_status()
            return RefreshTokenResponse(**res.json())
        except requests.exceptions.RequestException as e:
            print(f"Error refreshing token: {e}")
            raise

    def start_password_reset(
        self, request: PasswordResetRequest
    ) -> PasswordResetResponse:
        url = f"https://{self.domain}/dbconnections/change_password"
        payload = {
            "client_id": request.client_id,
            "email": request.email,
            "connection": request.connection,
        }
        try:
            res = requests.post(url, json=payload)
            res.raise_for_status()
            return PasswordResetResponse(
                message=res.json().get("message", "Password reset email sent")
            )
        except requests.exceptions.RequestException as e:
            print(f"Error starting password reset: {e}")
            raise
