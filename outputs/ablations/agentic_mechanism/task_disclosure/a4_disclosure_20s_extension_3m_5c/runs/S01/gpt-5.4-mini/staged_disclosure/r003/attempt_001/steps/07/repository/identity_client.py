import os
from typing import Any, Dict, Optional

import requests


GOOGLE_IDENTITY_TOOLKIT_URL = "https://identitytoolkit.googleapis.com/v1/accounts"


class IdentityClient:
    def __init__(self, api_key: Optional[str] = None, timeout: int = 30) -> None:
        self.api_key = api_key or os.getenv("FIREBASE_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise RuntimeError("FIREBASE_API_KEY or GOOGLE_API_KEY is required")
        self.timeout = timeout

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{GOOGLE_IDENTITY_TOOLKIT_URL}:{path}",
            params={"key": self.api_key},
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def register_user(self, email: str, password: str) -> Dict[str, Any]:
        return self._post(
            "signUp",
            {"email": email, "password": password, "returnSecureToken": True},
        )

    def login(self, email: str, password: str) -> Dict[str, Any]:
        return self._post(
            "signInWithPassword",
            {"email": email, "password": password, "returnSecureToken": True},
        )

    def start_password_reset(self, email: str) -> Dict[str, Any]:
        return self._post("sendOobCode", {"requestType": "PASSWORD_RESET", "email": email})

    def refresh_session(self, refresh_token: str) -> Dict[str, Any]:
        response = requests.post(
            "https://securetoken.googleapis.com/v1/token",
            params={"key": self.api_key},
            data={"grant_type": "refresh_token", "refresh_token": refresh_token},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()


def get_identity_client() -> IdentityClient:
    return IdentityClient()
