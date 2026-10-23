from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

from safety_models import normalize_text


@dataclass
class SafetyClientConfig:
    endpoint: str
    api_key: str
    api_version: str = "2024-09-01"


class AzureContentSafetyClient:
    def __init__(self, config: Optional[SafetyClientConfig] = None):
        endpoint = (config.endpoint if config else os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "")).rstrip("/")
        api_key = config.api_key if config else os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
        api_version = config.api_version if config else os.getenv("AZURE_CONTENT_SAFETY_API_VERSION", "2024-09-01")
        self.config = SafetyClientConfig(endpoint=endpoint, api_key=api_key, api_version=api_version)
        self.session = requests.Session()
        self.session.headers.update({
            "Ocp-Apim-Subscription-Key": self.config.api_key,
            "Content-Type": "application/json",
        })

    def _url(self, path: str) -> str:
        return f"{self.config.endpoint}{path}?api-version={self.config.api_version}"

    def post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self.session.post(self._url(path), json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def analyze_text(self, text: str, categories: Optional[list[str]] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"text": normalize_text(text)}
        if categories:
            body["categories"] = categories
        return self.post("/text:analyze", body)

    def analyze_batch(self, texts: list[str]) -> Dict[str, Any]:
        return self.post("/text:analyze-batch", {"texts": [normalize_text(t) for t in texts]})

    def redact(self, text: str) -> Dict[str, Any]:
        return self.post("/text:redact", {"text": normalize_text(text)})

    def threshold(self, scores: Dict[str, float], thresholds: Dict[str, float]) -> Dict[str, Any]:
        return self.post("/text:threshold", {"scores": scores, "thresholds": thresholds})
