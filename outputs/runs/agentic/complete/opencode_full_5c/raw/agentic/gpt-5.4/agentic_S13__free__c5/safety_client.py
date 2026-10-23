from __future__ import annotations

import os
from typing import Any

import requests


DEFAULT_AZURE_API_VERSION = "2024-09-01"
DEFAULT_AZURE_SAFETY_PATH = "/contentsafety/text:analyze"


def azure_content_safety_config() -> dict[str, str]:
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"].rstrip("/")
    api_key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    api_version = os.getenv(
        "AZURE_CONTENT_SAFETY_API_VERSION", DEFAULT_AZURE_API_VERSION
    )
    return {
        "endpoint": endpoint,
        "api_key": api_key,
        "api_version": api_version,
        "provider": "azure_content_safety",
    }


def azure_headers() -> dict[str, str]:
    config = azure_content_safety_config()
    return {
        "Ocp-Apim-Subscription-Key": config["api_key"],
        "Content-Type": "application/json",
    }


def azure_post(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    config = azure_content_safety_config()
    url = f"{config['endpoint']}{path}?api-version={config['api_version']}"
    response = requests.post(url, headers=azure_headers(), json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def openai_config() -> dict[str, str]:
    return {
        "api_key": os.environ["OPENAI_API_KEY"],
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "embedding_model": os.getenv(
            "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
        ),
        "tts_model": os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts"),
        "provider": "openai",
    }


def deepl_config() -> dict[str, str]:
    return {
        "api_key": os.environ["DEEPL_API_KEY"],
        "endpoint": os.getenv("DEEPL_API_URL", "https://api.deepl.com/v2/translate"),
        "provider": "deepl",
    }
