from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class SafetyConfig:
    endpoint: str
    key: str
    api_version: str = "2023-10-01"


def load_config() -> SafetyConfig:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "").rstrip("/")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are required")
    return SafetyConfig(endpoint=endpoint, key=key)


class ContentSafetyClient:
    def __init__(self, config: Optional[SafetyConfig] = None) -> None:
        self.config = config or load_config()
        self.session = requests.Session()
        self.session.headers.update({
            "Ocp-Apim-Subscription-Key": self.config.key,
            "Content-Type": "application/json",
        })

    def moderate_text(self, text: str) -> Dict[str, Any]:
        url = f"{self.config.endpoint}/contentsafety/text:analyze?api-version={self.config.api_version}"
        payload = {"text": text, "categories": ["Hate", "Sexual", "Violence", "SelfHarm"]}
        return self.session.post(url, json=payload, timeout=30).json()

    def analyze_batch(self, texts: list[str]) -> Dict[str, Any]:
        url = f"{self.config.endpoint}/contentsafety/text:analyze?api-version={self.config.api_version}"
        payload = {"text": "\n".join(texts), "categories": ["Hate", "Sexual", "Violence", "SelfHarm"]}
        return self.session.post(url, json=payload, timeout=30).json()
