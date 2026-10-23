import os
from typing import Optional

import requests


class SafetyClient:
    def __init__(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = 30,
    ):
        self.endpoint = (
            endpoint or os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT") or ""
        ).rstrip("/")
        self.api_key = api_key or os.getenv("AZURE_CONTENT_SAFETY_KEY") or ""
        self.timeout = timeout

    @property
    def headers(self):
        return {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def post(self, path: str, payload: dict):
        url = f"{self.endpoint}{path}"
        response = requests.post(
            url, json=payload, headers=self.headers, timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
