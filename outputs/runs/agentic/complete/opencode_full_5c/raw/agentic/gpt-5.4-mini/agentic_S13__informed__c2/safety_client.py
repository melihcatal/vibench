import os
from typing import Any, Dict, Optional

import requests


AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
AZURE_CONTENT_SAFETY_API_VERSION = "2023-10-01"


class SafetyClient:
    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        self.endpoint = (endpoint or AZURE_CONTENT_SAFETY_ENDPOINT).rstrip("/")
        self.key = key or AZURE_CONTENT_SAFETY_KEY

    def _headers(self) -> Dict[str, str]:
        return {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json",
        }

    def analyze_text(
        self, text: str, categories: Optional[list[str]] = None
    ) -> Dict[str, Any]:
        url = f"{self.endpoint}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"
        payload: Dict[str, Any] = {"text": text}
        if categories:
            payload["categories"] = categories
        response = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def analyze_batch(
        self, messages: list[str], categories: Optional[list[str]] = None
    ) -> Dict[str, Any]:
        return {
            "results": [
                self.analyze_text(message, categories=categories)
                for message in messages
            ]
        }
