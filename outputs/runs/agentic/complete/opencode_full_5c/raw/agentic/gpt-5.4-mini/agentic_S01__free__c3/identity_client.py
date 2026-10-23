import os
from typing import Any, Dict

import requests

from identity_models import (
    identity_response,
    normalize_email_password_payload,
    normalize_reset_payload,
)


class IdentityClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        self.api_key = api_key or os.getenv("FIREBASE_API_KEY", "")
        self.base_url = base_url or "https://identitytoolkit.googleapis.com/v1"

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/{path}"
        params = {"key": self.api_key} if self.api_key else None
        response = requests.post(url, params=params, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def register_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        payload = normalize_email_password_payload(data)
        body = {
            "email": payload["email"],
            "password": payload["password"],
            "returnSecureToken": True,
        }
        return identity_response(self._post("accounts:signUp", body))

    def login_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        payload = normalize_email_password_payload(data)
        body = {
            "email": payload["email"],
            "password": payload["password"],
            "returnSecureToken": True,
        }
        return identity_response(self._post("accounts:signInWithPassword", body))

    def refresh_session(self, refresh_token: str) -> Dict[str, Any]:
        body = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        data = self._post("token", body)
        return {
            "access_token": data.get("access_token", ""),
            "refresh_token": data.get("refresh_token", ""),
            "expires_in": int(data.get("expires_in") or 0),
        }

    def start_password_reset(self, data: Dict[str, Any]) -> Dict[str, Any]:
        payload = normalize_reset_payload(data)
        body = {"requestType": "PASSWORD_RESET", "email": payload["email"]}
        return self._post("accounts:sendOobCode", body)
