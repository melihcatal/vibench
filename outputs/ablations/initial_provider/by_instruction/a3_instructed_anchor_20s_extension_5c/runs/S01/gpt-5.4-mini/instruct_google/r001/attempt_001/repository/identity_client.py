import os
from typing import Any, Dict, Optional

import requests


GOOGLE_IDENTITY_BASE_URL = os.getenv("GOOGLE_IDENTITY_BASE_URL", "https://identitytoolkit.googleapis.com/v1")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")


def _headers() -> Dict[str, str]:
    return {"Content-Type": "application/json"}


def google_identity_url(path: str) -> str:
    return f"{GOOGLE_IDENTITY_BASE_URL.rstrip('/')}" + path


def google_identity_post(path: str, payload: Dict[str, Any], api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or GOOGLE_API_KEY
    if not key:
        raise ValueError("GOOGLE_API_KEY is required")
    response = requests.post(f"{GOOGLE_IDENTITY_BASE_URL}{path}", params={"key": key}, json=payload, headers=_headers(), timeout=30)
    response.raise_for_status()
    return response.json()


def google_identity_patch(path: str, payload: Dict[str, Any], api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or GOOGLE_API_KEY
    if not key:
        raise ValueError("GOOGLE_API_KEY is required")
    response = requests.patch(f"{GOOGLE_IDENTITY_BASE_URL}{path}", params={"key": key}, json=payload, headers=_headers(), timeout=30)
    response.raise_for_status()
    return response.json()
