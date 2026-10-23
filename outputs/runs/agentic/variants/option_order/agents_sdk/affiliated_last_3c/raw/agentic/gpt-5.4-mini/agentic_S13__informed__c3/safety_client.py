from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from requests import Session

PERSPECTIVE_API_BASE = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
AZURE_CONTENT_SAFETY_BASE = "https://{endpoint}.cognitiveservices.azure.com"


@dataclass
class SafetyClientConfig:
    provider: str
    api_key: str
    endpoint: Optional[str] = None
    extra: Dict[str, Any] = None

    @staticmethod
    def from_env(provider: str) -> "SafetyClientConfig":
        provider = provider.lower()
        if provider == "perspective":
            return SafetyClientConfig(provider="perspective", api_key=os.environ.get("PERSPECTIVE_API_KEY", ""), extra={})
        if provider == "azure":
            return SafetyClientConfig(
                provider="azure",
                api_key=os.environ.get("AZURE_CONTENT_SAFETY_KEY", ""),
                endpoint=os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT"),
                extra={},
            )
        raise ValueError(f"Unsupported provider: {provider}")


class SafetyHTTPClient:
    def __init__(self, config: SafetyClientConfig, session: Optional[Session] = None):
        self.config = config
        self.session = session or requests.Session()

    def post(self, url: str, json: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        response = self.session.post(url, json=json, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def perspective_headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/json"}

    def azure_headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": self.config.api_key}
