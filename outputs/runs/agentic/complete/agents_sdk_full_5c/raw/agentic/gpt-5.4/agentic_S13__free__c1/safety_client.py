from __future__ import annotations

import os
from typing import Any, Dict, Optional

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


DEFAULT_OUTPUT_TYPE = "FourSeverityLevels"


def get_content_safety_client() -> ContentSafetyClient:
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    return ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def get_openai_headers() -> Dict[str, str]:
    api_key = os.environ["OPENAI_API_KEY"]
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def get_openai_base_url() -> str:
    return os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")


def get_deepl_headers() -> Dict[str, str]:
    return {
        "Authorization": f"DeepL-Auth-Key {os.environ['DEEPL_API_KEY']}",
        "Content-Type": "application/json",
    }


def get_deepl_base_url() -> str:
    return os.environ.get("DEEPL_BASE_URL", "https://api.deepl.com/v2")


def build_thresholds(overrides: Optional[Dict[str, int]] = None) -> Dict[str, int]:
    thresholds = {
        "hate": int(os.environ.get("SAFETY_THRESHOLD_HATE", "2")),
        "sexual": int(os.environ.get("SAFETY_THRESHOLD_SEXUAL", "2")),
        "self_harm": int(os.environ.get("SAFETY_THRESHOLD_SELF_HARM", "1")),
        "violence": int(os.environ.get("SAFETY_THRESHOLD_VIOLENCE", "2")),
    }
    if overrides:
        thresholds.update({k: int(v) for k, v in overrides.items()})
    return thresholds


def compact_json_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in payload.items() if v is not None}
