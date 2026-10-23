from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


DEFAULT_ENDPOINT = "https://{resource_name}.cognitiveservices.azure.com"
DEFAULT_API_VERSION = "2024-02-15-preview"


@dataclass(frozen=True)
class TextContentSafetyConfig:
    endpoint: str
    api_key: str
    api_version: str = DEFAULT_API_VERSION
    resource_name: Optional[str] = None


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def load_config() -> TextContentSafetyConfig:
    endpoint = _env("AZURE_AI_CONTENT_SAFETY_ENDPOINT") or _env("AZURE_CONTENT_SAFETY_ENDPOINT")
    resource_name = _env("AZURE_AI_CONTENT_SAFETY_RESOURCE_NAME") or _env("AZURE_CONTENT_SAFETY_RESOURCE_NAME")
    api_key = _env("AZURE_AI_CONTENT_SAFETY_API_KEY") or _env("AZURE_CONTENT_SAFETY_API_KEY")
    api_version = _env("AZURE_AI_CONTENT_SAFETY_API_VERSION", DEFAULT_API_VERSION)

    if not api_key:
        raise ValueError("Missing Azure AI Content Safety API key")

    if not endpoint and resource_name:
        endpoint = DEFAULT_ENDPOINT.format(resource_name=resource_name)

    if not endpoint:
        raise ValueError("Missing Azure AI Content Safety endpoint or resource name")

    endpoint = endpoint.rstrip("/")
    return TextContentSafetyConfig(endpoint=endpoint, api_key=api_key, api_version=api_version or DEFAULT_API_VERSION, resource_name=resource_name)


class TextContentSafetyClient:
    def __init__(self, config: Optional[TextContentSafetyConfig] = None, session: Optional[requests.Session] = None):
        self.config = config or load_config()
        self.session = session or requests.Session()

    def _headers(self) -> Dict[str, str]:
        return {
            "Ocp-Apim-Subscription-Key": self.config.api_key,
            "Content-Type": "application/json",
        }

    def _url(self, path: str) -> str:
        return f"{self.config.endpoint}{path}?api-version={self.config.api_version}"

    def post(self, path: str, payload: Dict[str, Any], timeout: float = 30.0) -> Dict[str, Any]:
        response = self.session.post(self._url(path), headers=self._headers(), json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json()

    def analyze_text(self, text: str, *, categories: Optional[list[str]] = None, blocklist_names: Optional[list[str]] = None, output_type: str = "FourSeverityLevels", timeout: float = 30.0) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"text": text, "outputType": output_type}
        if categories is not None:
            payload["categories"] = categories
        if blocklist_names is not None:
            payload["blocklistNames"] = blocklist_names
        return self.post("/contentsafety/text:analyze", payload, timeout=timeout)

    def analyze_image(self, image_url: str, *, categories: Optional[list[str]] = None, timeout: float = 30.0) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"image": {"url": image_url}, "outputType": "FourSeverityLevels"}
        if categories is not None:
            payload["categories"] = categories
        return self.post("/contentsafety/image:analyze", payload, timeout=timeout)
