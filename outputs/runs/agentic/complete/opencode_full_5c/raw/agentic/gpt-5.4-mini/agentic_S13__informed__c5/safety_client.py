import os
from typing import Optional

import requests


class AzureContentSafetyClient:
    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        self.endpoint = (
            endpoint or os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "")
        ).rstrip("/")
        self.key = key or os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
        self.session = requests.Session()
        self.session.headers.update(
            {"Ocp-Apim-Subscription-Key": self.key, "Content-Type": "application/json"}
        )

    def post(self, path: str, payload: dict) -> dict:
        response = self.session.post(f"{self.endpoint}{path}", json=payload, timeout=30)
        response.raise_for_status()
        return response.json()


def get_client() -> AzureContentSafetyClient:
    return AzureContentSafetyClient()
