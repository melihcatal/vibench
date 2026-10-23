from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

import requests


AZURE_AI_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_AI_CONTENT_SAFETY_ENDPOINT", "").rstrip("/")
AZURE_AI_CONTENT_SAFETY_API_KEY = os.getenv("AZURE_AI_CONTENT_SAFETY_API_KEY", "")
AZURE_AI_CONTENT_SAFETY_API_VERSION = os.getenv("AZURE_AI_CONTENT_SAFETY_API_VERSION", "2024-09-01")


@dataclass(frozen=True)
class SafetyClientConfig:
    endpoint: str = AZURE_AI_CONTENT_SAFETY_ENDPOINT
    api_key: str = AZURE_AI_CONTENT_SAFETY_API_KEY
    api_version: str = AZURE_AI_CONTENT_SAFETY_API_VERSION

    def is_configured(self) -> bool:
        return bool(self.endpoint and self.api_key)

    @classmethod
    def from_env(cls) -> "SafetyClientConfig":
        return cls()


def get_config() -> SafetyClientConfig:
    return SafetyClientConfig.from_env()


def require_config(config: Optional[SafetyClientConfig] = None) -> SafetyClientConfig:
    cfg = config or get_config()
    if not cfg.endpoint or not cfg.api_key:
        raise RuntimeError("AZURE_AI_CONTENT_SAFETY_ENDPOINT and AZURE_AI_CONTENT_SAFETY_API_KEY are required")
    return cfg


def build_headers(config: Optional[SafetyClientConfig] = None) -> Dict[str, str]:
    cfg = require_config(config)
    return {
        "Ocp-Apim-Subscription-Key": cfg.api_key,
        "Content-Type": "application/json",
    }


def build_text_analyze_url(config: Optional[SafetyClientConfig] = None) -> str:
    cfg = require_config(config)
    return f"{cfg.endpoint}/contentsafety/text:analyze?api-version={cfg.api_version}"


def post_json(path: str, payload: Mapping[str, Any], config: Optional[SafetyClientConfig] = None, timeout: int = 30) -> Dict[str, Any]:
    cfg = require_config(config)
    base = cfg.endpoint
    if not path.startswith("/"):
        path = "/" + path
    response = requests.post(
        f"{base}{path}",
        headers=build_headers(cfg),
        json=dict(payload),
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def analyze_text(text: str, config: Optional[SafetyClientConfig] = None, timeout: int = 30) -> Dict[str, Any]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    cfg = require_config(config)
    response = requests.post(
        build_text_analyze_url(cfg),
        headers=build_headers(cfg),
        json={"text": text},
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def normalize_severity(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        mapping = {"safe": 0, "low": 1, "medium": 2, "high": 3, "very_high": 4}
        if normalized in mapping:
            return mapping[normalized]
        try:
            return int(float(normalized))
        except ValueError:
            return 0
    return 0


def extract_category_severities(result: Mapping[str, Any]) -> Dict[str, int]:
    severities: Dict[str, int] = {}
    for category, value in result.items():
        if isinstance(value, Mapping):
            for key in ("severity", "level", "score"):
                if key in value:
                    severities[category] = normalize_severity(value[key])
                    break
        else:
            severities[category] = normalize_severity(value)
    return severities
