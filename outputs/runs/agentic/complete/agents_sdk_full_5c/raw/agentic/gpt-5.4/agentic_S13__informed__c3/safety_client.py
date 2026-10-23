from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


DEFAULT_API_VERSION = "2024-09-01"
DEFAULT_PROVIDER = "azure-ai-content-safety"
DEFAULT_KIND = "text:analyze"


def get_azure_content_safety_config() -> Dict[str, str]:
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"].rstrip("/")
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    api_version = os.getenv("AZURE_CONTENT_SAFETY_API_VERSION", DEFAULT_API_VERSION)
    return {
        "endpoint": endpoint,
        "key": key,
        "api_version": api_version,
        "provider": DEFAULT_PROVIDER,
    }


def build_analyze_url() -> str:
    cfg = get_azure_content_safety_config()
    return f"{cfg['endpoint']}/contentsafety/text:analyze?api-version={cfg['api_version']}"


def build_headers() -> Dict[str, str]:
    cfg = get_azure_content_safety_config()
    return {
        "Ocp-Apim-Subscription-Key": cfg["key"],
        "Content-Type": "application/json",
    }


def analyze_text(text: str, *, output_type: Optional[str] = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"text": text}
    if output_type:
        payload["outputType"] = output_type
    response = requests.post(build_analyze_url(), headers=build_headers(), json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
