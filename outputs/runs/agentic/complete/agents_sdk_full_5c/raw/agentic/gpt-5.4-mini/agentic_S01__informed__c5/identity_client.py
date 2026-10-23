from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any, Dict, Optional

import requests

from identity_models import (
    EmailPasswordAccountRequest,
    PasswordResetRequest,
    TokenResponse,
    normalize_email,
)


class IdentityClient:
    """IBM Cloud App ID REST helper."""

    def __init__(self, domain: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        self.domain = domain or os.getenv("IBM_APPID_DOMAIN")
        self.client_id = client_id or os.getenv("IBM_APPID_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("IBM_APPID_CLIENT_SECRET")
        self.base_url = f"https://{self.domain}/management/v4" if self.domain else None

    def _headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/json", "Accept": "application/json"}

    def _request(self, method: str, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self.base_url:
            raise RuntimeError("IBM App ID domain is not configured")
        auth = (self.client_id or "", self.client_secret or "")
        response = requests.request(method, f"{self.base_url}{path}", headers=self._headers(), auth=auth, json=json, timeout=30)
        response.raise_for_status()
        return response.json() if response.content else {}

    def register_user(self, request: EmailPasswordAccountRequest) -> Dict[str, Any]:
        payload = asdict(request)
        payload["email"] = normalize_email(request.email)
        return self._request("POST", "/users", json=payload)

    def login(self, email: str, password: str) -> TokenResponse:
        body = {"username": normalize_email(email), "password": password, "grant_type": "password"}
        data = self._request("POST", "/token", json=body)
        return TokenResponse(access_token=data.get("access_token", ""), refresh_token=data.get("refresh_token"), expires_in=data.get("expires_in"), token_type=data.get("token_type", "Bearer"), raw=data)

    def refresh(self, refresh_token: str) -> TokenResponse:
        data = self._request("POST", "/token/refresh", json={"refresh_token": refresh_token})
        return TokenResponse(access_token=data.get("access_token", ""), refresh_token=data.get("refresh_token", refresh_token), expires_in=data.get("expires_in"), token_type=data.get("token_type", "Bearer"), raw=data)

    def password_reset(self, request: PasswordResetRequest) -> Dict[str, Any]:
        payload = {"email": normalize_email(request.email), "locale": request.locale}
        return self._request("POST", "/users/password/reset", json=payload)
