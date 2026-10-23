from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


def get_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def hive_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Token {get_env('HIVE_API_KEY')}",
        "Content-Type": "application/json",
    }


def hive_post(path: str, payload: Dict[str, Any], timeout: int = 30) -> Dict[str, Any]:
    base_url = os.getenv("HIVE_API_BASE", "https://api.thehive.ai")
    response = requests.post(
        f"{base_url}{path}", headers=hive_headers(), json=payload, timeout=timeout
    )
    response.raise_for_status()
    return response.json()


def deepgram_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Token {get_env('DEEPGRAM_API_KEY')}",
        "Content-Type": "application/json",
    }


def deepgram_post(
    path: str, payload: Dict[str, Any], timeout: int = 60
) -> requests.Response:
    base_url = os.getenv("DEEPGRAM_API_BASE", "https://api.deepgram.com")
    response = requests.post(
        f"{base_url}{path}", headers=deepgram_headers(), json=payload, timeout=timeout
    )
    response.raise_for_status()
    return response


def openai_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {get_env('OPENAI_API_KEY')}",
        "Content-Type": "application/json",
    }


def openai_post(
    path: str, payload: Dict[str, Any], timeout: int = 60
) -> Dict[str, Any]:
    base_url = os.getenv("OPENAI_API_BASE", "https://api.openai.com")
    response = requests.post(
        f"{base_url}{path}", headers=openai_headers(), json=payload, timeout=timeout
    )
    response.raise_for_status()
    return response.json()


def openai_get_embedding_model() -> str:
    return os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")


def openai_get_translation_model() -> str:
    return os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def openai_get_summary_model() -> str:
    return os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini")
