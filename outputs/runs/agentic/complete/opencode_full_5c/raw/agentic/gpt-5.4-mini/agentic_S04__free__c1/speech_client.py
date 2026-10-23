import os
from typing import Any, Dict, Optional

import requests


def get_openai_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return key


def get_base_url() -> str:
    return os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")


def headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {get_openai_api_key()}",
        "Content-Type": "application/json",
    }


def post(
    path: str, payload: Dict[str, Any], timeout: Optional[int] = 60
) -> Dict[str, Any]:
    r = requests.post(
        f"{get_base_url().rstrip('/')}{path}",
        headers=headers(),
        json=payload,
        timeout=timeout,
    )
    r.raise_for_status()
    return r.json()


def get(path: str, timeout: Optional[int] = 60) -> Dict[str, Any]:
    r = requests.get(
        f"{get_base_url().rstrip('/')}{path}", headers=headers(), timeout=timeout
    )
    r.raise_for_status()
    return r.json()
