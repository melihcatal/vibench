from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"
AZURE_CONTENT_SAFETY_V1_PATH = "/contentsafety/text:analysis?api-version=2024-09-01"


@dataclass(frozen=True)
class SafetyClientConfig:
    endpoint: str
    api_key: str
    api_version: str = "2024-09-01"

    @classmethod
    def from_env(cls) -> "SafetyClientConfig":
        endpoint = os.getenv(AZURE_CONTENT_SAFETY_ENDPOINT_ENV, "").rstrip("/")
        api_key = os.getenv(AZURE_CONTENT_SAFETY_KEY_ENV, "")
        if not endpoint:
            raise RuntimeError(f"Missing {AZURE_CONTENT_SAFETY_ENDPOINT_ENV}")
        if not api_key:
            raise RuntimeError(f"Missing {AZURE_CONTENT_SAFETY_KEY_ENV}")
        return cls(endpoint=endpoint, api_key=api_key)


class SafetyClient:
    def __init__(self, config: Optional[SafetyClientConfig] = None) -> None:
        self.config = config or SafetyClientConfig.from_env()
        self._session = requests.Session()
        self._session.headers.update({
            "Ocp-Apim-Subscription-Key": self.config.api_key,
            "Content-Type": "application/json",
        })

    @property
    def base_url(self) -> str:
        return self.config.endpoint.rstrip("/")

    def post(self, path: str, payload: Dict[str, Any]) -> requests.Response:
        url = f"{self.base_url}{path}"
        response = self._session.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response

    def moderate_text(self, text: str) -> Dict[str, Any]:
        payload = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}
        return self.post(AZURE_CONTENT_SAFETY_V1_PATH, payload).json()

    def moderate_batch(self, texts: list[str]) -> Dict[str, Any]:
        payload = {"items": [{"text": text, "id": str(i)} for i, text in enumerate(texts)]}
        return self.post("/contentsafety/text/batch:analysis?api-version=2024-09-01", payload).json()

    def close(self) -> None:
        self._session.close()
