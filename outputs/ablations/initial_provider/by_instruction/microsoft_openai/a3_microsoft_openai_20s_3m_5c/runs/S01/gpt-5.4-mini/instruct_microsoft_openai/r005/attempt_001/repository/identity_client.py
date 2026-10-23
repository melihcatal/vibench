import os
from typing import Any, Dict

import requests

from identity_models import AccountRequest, ResetRequest, coerce_token_response, env


class IdentityClient:
    def __init__(self) -> None:
        self.base_url = env("MICROSOFT_ENTRA_IDENTITY_BASE_URL", "https://graph.microsoft.com/v1.0")
        self.tenant_id = env("AZURE_TENANT_ID")
        self.client_id = env("AZURE_CLIENT_ID")
        self.client_secret = env("AZURE_CLIENT_SECRET")
        self.session = requests.Session()

    def _headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/json"}

    def create_user(self, request: AccountRequest) -> Dict[str, Any]:
        payload = {"mailNickname": request.email.split("@")[0], "userPrincipalName": request.email, "passwordProfile": {"password": request.password, "forceChangePasswordNextSignIn": False}, "accountEnabled": True}
        response = self.session.post(f"{self.base_url}/users", json=payload, headers=self._headers(), timeout=30)
        response.raise_for_status()
        return response.json()

    def password_login(self, request: AccountRequest) -> Dict[str, Any]:
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        data = {"client_id": self.client_id, "client_secret": self.client_secret, "grant_type": "password", "username": request.email, "password": request.password, "scope": "openid profile offline_access"}
        response = self.session.post(token_url, data=data, timeout=30)
        response.raise_for_status()
        return coerce_token_response(response.json()).raw or {}

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        data = {"client_id": self.client_id, "client_secret": self.client_secret, "grant_type": "refresh_token", "refresh_token": refresh_token, "scope": "openid profile offline_access"}
        response = self.session.post(token_url, data=data, timeout=30)
        response.raise_for_status()
        return response.json()

    def start_password_reset(self, request: ResetRequest) -> Dict[str, Any]:
        payload = {"email": request.email, "client_id": self.client_id}
        response = self.session.post(f"{self.base_url}/users/{request.email}/sendMail", json=payload, headers=self._headers(), timeout=30)
        response.raise_for_status()
        return response.json()
