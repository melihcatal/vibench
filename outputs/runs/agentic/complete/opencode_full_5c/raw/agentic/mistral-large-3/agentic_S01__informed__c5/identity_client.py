import os
from typing import Dict, Any
import requests
from identity_models import (
    RegisterRequest,
    RegisterResponse,
    normalize_register_response,
    LoginResponse,
    RefreshResponse,
    PasswordResetResponse,
    normalize_login_response,
    normalize_refresh_response,
    normalize_password_reset_response,
)


class IBMAppIDClient:
    def __init__(self):
        self.client_id = os.getenv("IBM_APPID_CLIENT_ID")
        self.client_secret = os.getenv("IBM_APPID_CLIENT_SECRET")
        self.tenant_id = os.getenv("IBM_APPID_TENANT_ID")
        self.region = os.getenv("IBM_APPID_REGION", "us-south")
        self.token_url = (
            f"https://{self.region}.appid.cloud.ibm.com/oauth/v4/{self.tenant_id}/token"
        )
        self.register_url = f"https://{self.region}.appid.cloud.ibm.com/management/v4/{self.tenant_id}/cloud_directory/sign_up"
        self.login_url = (
            f"https://{self.region}.appid.cloud.ibm.com/oauth/v4/{self.tenant_id}/token"
        )
        self.refresh_url = (
            f"https://{self.region}.appid.cloud.ibm.com/oauth/v4/{self.tenant_id}/token"
        )
        self.reset_url = f"https://{self.region}.appid.cloud.ibm.com/management/v4/{self.tenant_id}/cloud_directory/forgot_password"
        self._access_token = None

    def _get_management_token(self) -> str:
        if self._access_token:
            return self._access_token

        response = requests.post(
            self.token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        self._access_token = response.json()["access_token"]
        return self._access_token

    def register_user(self, request: RegisterRequest) -> RegisterResponse:
        token = self._get_management_token()
        response = requests.post(
            self.register_url,
            json={
                "email": request.email,
                "password": request.password,
                "username": request.email,
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        response.raise_for_status()
        return normalize_register_response(response.json())

    def email_password_login(self, request: LoginRequest) -> LoginResponse:
        response = requests.post(
            self.login_url,
            data={
                "grant_type": "password",
                "username": request.email,
                "password": request.password,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        return normalize_login_response(response.json())

    def refresh_session(self, request: RefreshRequest) -> RefreshResponse:
        response = requests.post(
            self.refresh_url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": request.refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        return normalize_refresh_response(response.json())

    def password_reset(self, request: PasswordResetRequest) -> PasswordResetResponse:
        token = self._get_management_token()
        response = requests.post(
            self.reset_url,
            json={"email": request.email},
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        response.raise_for_status()
        return normalize_password_reset_response(response.json())
