import os
from typing import Any, Dict

import requests

from identity_models import normalize_email, normalize_locale


class IdentityClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    @classmethod
    def from_env(cls) -> "IdentityClient":
        return cls(
            os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1"),
            os.environ.get("OPENAI_API_KEY", ""),
        )

    def post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}{path}",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


def build_identity_payload(email: str, password: str, locale: str = "en") -> Dict[str, Any]:
    return {
        "email": normalize_email(email),
        "password": password,
        "locale": normalize_locale(locale),
    }
