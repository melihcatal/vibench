from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"


@dataclass(frozen=True)
class SafetyClientConfig:
    endpoint: str
    key: str
    api_version: str = "2023-10-01"

    @classmethod
    def from_env(cls) -> "SafetyClientConfig":
        endpoint = os.environ.get(AZURE_CONTENT_SAFETY_ENDPOINT_ENV, "").rstrip("/")
        key = os.environ.get(AZURE_CONTENT_SAFETY_KEY_ENV, "")
        if not endpoint or not key:
            raise ValueError("Azure AI Content Safety credentials are required")
        return cls(endpoint=endpoint, key=key)


class SafetyClient:
    def __init__(self, config: Optional[SafetyClientConfig] = None) -> None:
        self.config = config or SafetyClientConfig.from_env()
        self._session = requests.Session()
        self._session.headers.update({"Ocp-Apim-Subscription-Key": self.config.key})

    def _url(self, path: str) -> str:
        return f"{self.config.endpoint}{path}"

    def analyze_text(self, text: str) -> Dict[str, Any]:
        url = self._url(f"/contentsafety/text:analyze?api-version={self.config.api_version}")
        response = self._session.post(url, json={"text": text}, timeout=30)
        response.raise_for_status()
        return response.json()

    def analyze_batch(self, texts: list[str]) -> Dict[str, Any]:
        url = self._url(f"/contentsafety/text:analyze?api-version={self.config.api_version}")
        payload = {"text": t} for t in texts
        response = self._session.post(url, json={"documents": list(payload)}, timeout=30)
        response.raise_for_status()
        return response.json()

    def detect_pii(self, text: str) -> Dict[str, Any]:
        url = self._url(f"/contentsafety/text:detectPiiEntities?api-version={self.config.api_version}")
        response = self._session.post(url, json={"text": text}, timeout=30)
        response.raise_for_status()
        return response.json()
