from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"
AZURE_CONTENT_SAFETY_API_VERSION = "2024-09-01"


class AzureContentSafetyClient:
    def __init__(self, endpoint: Optional[str] = None, api_key: Optional[str] = None, timeout: int = 30):
        self.endpoint = (endpoint or os.environ[AZURE_CONTENT_SAFETY_ENDPOINT_ENV] or "").rstrip("/")
        self.api_key = api_key or os.environ[AZURE_CONTENT_SAFETY_KEY_ENV]
        self.timeout = timeout
        if not self.endpoint or not self.api_key:
            raise ValueError("Azure AI Content Safety endpoint and key are required")

    def _headers(self) -> Dict[str, str]:
        return {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def _url(self, path: str) -> str:
        return f"{self.endpoint}{path}?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"

    def analyze_text(self, text: str, categories: Optional[list[str]] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"text": text}
        if categories:
            payload["categories"] = categories
        response = requests.post(
            self._url("/contentsafety/text:analyze"),
            headers=self._headers(),
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def shield_text(self, text: str) -> Dict[str, Any]:
        response = requests.post(
            self._url("/contentsafety/text:shield"),
            headers=self._headers(),
            json={"text": text},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
