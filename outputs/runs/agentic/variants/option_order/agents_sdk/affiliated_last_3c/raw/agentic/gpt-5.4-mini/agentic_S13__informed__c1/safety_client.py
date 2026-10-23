from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

from safety_models import normalize_text


@dataclass
class SafetyConfig:
    endpoint: str = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    key: str = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
    api_version: str = os.getenv("AZURE_CONTENT_SAFETY_API_VERSION", "2024-09-01")


class SafetyClient:
    def __init__(self, config: Optional[SafetyConfig] = None) -> None:
        self.config = config or SafetyConfig()
        if self.config.endpoint and self.config.key:
            self.client = ContentSafetyClient(self.config.endpoint, AzureKeyCredential(self.config.key))
        else:
            self.client = None

    def rest_headers(self) -> Dict[str, str]:
        return {"Ocp-Apim-Subscription-Key": self.config.key, "Content-Type": "application/json"}

    def moderate_url(self) -> str:
        return f"{self.config.endpoint}/contentsafety/text:analyze?api-version={self.config.api_version}"

    def normalize(self, text: str) -> str:
        return normalize_text(text)

    def post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(self.moderate_url(), headers=self.rest_headers(), json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
