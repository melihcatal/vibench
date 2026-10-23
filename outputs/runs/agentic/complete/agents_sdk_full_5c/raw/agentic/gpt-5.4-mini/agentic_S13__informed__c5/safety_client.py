import os
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass(frozen=True)
class SafetyClientConfig:
    endpoint: str
    api_key: str

    @classmethod
    def from_env(cls) -> "SafetyClientConfig":
        endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "").rstrip("/")
        api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
        if not endpoint:
            raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT is required")
        if not api_key:
            raise ValueError("AZURE_CONTENT_SAFETY_KEY is required")
        return cls(endpoint=endpoint, api_key=api_key)


class AzureContentSafetyClient:
    def __init__(self, config: Optional[SafetyClientConfig] = None):
        self.config = config or SafetyClientConfig.from_env()
        self.session = requests.Session()
        self.session.headers.update({
            "Ocp-Apim-Subscription-Key": self.config.api_key,
            "Content-Type": "application/json",
        })

    def post(self, path: str, payload: dict) -> dict:
        url = f"{self.config.endpoint}{path}"
        response = self.session.post(url, json=payload, timeout=30)
        response.raise_for_status()
        if response.text:
            return response.json()
        return {}
