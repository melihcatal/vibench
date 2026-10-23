from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


class FirebaseIdentityClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.api_key = api_key or os.environ["FIREBASE_WEB_API_KEY"]
        self.session = session or requests.Session()
        self.base_url = "https://identitytoolkit.googleapis.com/v1"
        self.secure_token_url = "https://securetoken.googleapis.com/v1"

    def _post_json(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self.session.post(url, params={"key": self.api_key}, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def post_identity(self, method: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._post_json(f"{self.base_url}/{method}", payload)

    def post_secure_token(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self.session.post(
            f"{self.secure_token_url}/token",
            params={"key": self.api_key},
            data=payload,
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


def get_project_locale(default_locale: str = "en") -> str:
    return os.getenv("DEFAULT_ONBOARDING_LOCALE", default_locale)
