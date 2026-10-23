import os
from typing import Any, Dict, Optional

import requests


class ObservabilityClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("DD_API_KEY", "")
        self.app_key = os.getenv("DD_APP_KEY", "")
        self.site = os.getenv("DD_SITE", "datadoghq.com")
        self.base_url = f"https://api.{self.site}"

    def headers(self) -> Dict[str, str]:
        return {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
            "Content-Type": "application/json",
        }

    def post(self, path: str, payload: Dict[str, Any]) -> requests.Response:
        return requests.post(
            f"{self.base_url}{path}", headers=self.headers(), json=payload, timeout=30
        )

    def get(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        return requests.get(
            f"{self.base_url}{path}", headers=self.headers(), params=params, timeout=30
        )


def create_client() -> ObservabilityClient:
    return ObservabilityClient()
