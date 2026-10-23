from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

ASSEMBLYAI_API_BASE = os.getenv("ASSEMBLYAI_API_BASE", "https://api.assemblyai.com/v2")
ASSEMBLYAI_API_KEY_ENV = "ASSEMBLYAI_API_KEY"


def get_assemblyai_api_key() -> str:
    api_key = os.getenv(ASSEMBLYAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"Missing required environment variable: {ASSEMBLYAI_API_KEY_ENV}")
    return api_key


def get_assemblyai_headers(extra_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    headers = {
        "authorization": get_assemblyai_api_key(),
        "content-type": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)
    return headers


def assemblyai_post(path: str, payload: Dict[str, Any], timeout: int = 60) -> Dict[str, Any]:
    response = requests.post(
        f"{ASSEMBLYAI_API_BASE}{path}",
        json=payload,
        headers=get_assemblyai_headers(),
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def assemblyai_get(path: str, timeout: int = 60) -> Dict[str, Any]:
    response = requests.get(
        f"{ASSEMBLYAI_API_BASE}{path}",
        headers=get_assemblyai_headers(),
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()
