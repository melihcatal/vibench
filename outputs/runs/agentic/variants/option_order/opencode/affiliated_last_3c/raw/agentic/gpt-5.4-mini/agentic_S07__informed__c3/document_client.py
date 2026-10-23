import os
from typing import Any, Dict, Optional


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def get_azure_document_intelligence_config() -> Dict[str, str]:
    return {
        "endpoint": _env("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
        "key": _env("AZURE_DOCUMENT_INTELLIGENCE_KEY"),
        "api_version": _env("AZURE_DOCUMENT_INTELLIGENCE_API_VERSION", "2024-11-30"),
    }


def get_openai_config() -> Dict[str, str]:
    return {
        "api_key": _env("OPENAI_API_KEY"),
        "model": _env("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
    }


def get_deepl_config() -> Dict[str, str]:
    return {
        "auth_key": _env("DEEPL_AUTH_KEY"),
        "base_url": _env("DEEPL_BASE_URL", "https://api-free.deepl.com"),
    }


def get_perspective_config() -> Dict[str, str]:
    return {
        "api_key": _env("PERSPECTIVE_API_KEY"),
        "base_url": _env(
            "PERSPECTIVE_BASE_URL", "https://commentanalyzer.googleapis.com"
        ),
    }


def get_azure_contentsafety_config() -> Dict[str, str]:
    return {
        "endpoint": _env("AZURE_CONTENT_SAFETY_ENDPOINT"),
        "key": _env("AZURE_CONTENT_SAFETY_KEY"),
        "api_version": _env("AZURE_CONTENT_SAFETY_API_VERSION", "2024-09-01"),
    }


def pick_text(data: Any, default: str = "") -> str:
    if isinstance(data, dict):
        for key in ("text", "content", "translated_text", "output", "result"):
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    if isinstance(data, str) and data.strip():
        return data.strip()
    return default
