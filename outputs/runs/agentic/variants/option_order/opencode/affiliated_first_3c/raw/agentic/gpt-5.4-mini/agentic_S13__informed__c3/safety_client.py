import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class SafetyClientConfig:
    endpoint: str
    api_key: str
    api_version: str = "2023-10-01"


def load_config() -> SafetyClientConfig:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "").rstrip("/")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    api_version = os.environ.get("AZURE_CONTENT_SAFETY_API_VERSION", "2023-10-01")
    return SafetyClientConfig(endpoint=endpoint, api_key=api_key, api_version=api_version)


class SafetyClient:
    def __init__(self, config: Optional[SafetyClientConfig] = None):
        self.config = config or load_config()
        self.session = requests.Session()

    def _headers(self) -> Dict[str, str]:
        return {"Ocp-Apim-Subscription-Key": self.config.api_key, "Content-Type": "application/json"}

    def post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.config.endpoint}{path}"
        response = self.session.post(url, params={"api-version": self.config.api_version}, headers=self._headers(), json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
