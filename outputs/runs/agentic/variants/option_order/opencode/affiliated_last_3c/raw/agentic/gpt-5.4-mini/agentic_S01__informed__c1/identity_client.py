import os
from typing import Any, Dict

import requests

from identity_models import normalize_email, normalize_locale


class IdentityClient:
    def __init__(self, base_url: str | None = None, api_key: str | None = None):
        self.base_url = (
            base_url or os.environ.get("AUTH0_DOMAIN", "https://example.auth0.com")
        ).rstrip("/")
        self.api_key = api_key or os.environ.get("AUTH0_CLIENT_ID", "")

    def post(self, path: str, json: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}{path}",
            json=json,
            timeout=30,
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        return response.json()


def build_client() -> IdentityClient:
    return IdentityClient()


def normalize_account(email: str, locale: str | None = None) -> Dict[str, str]:
    return {"email": normalize_email(email), "locale": normalize_locale(locale)}
