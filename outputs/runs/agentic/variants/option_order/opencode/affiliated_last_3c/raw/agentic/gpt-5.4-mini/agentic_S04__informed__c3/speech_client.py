import os
from typing import Any, Dict

import requests


ASSEMBLYAI_API_URL = "https://api.assemblyai.com/v2"


def api_key() -> str:
    key = os.getenv("ASSEMBLYAI_API_KEY")
    if not key:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")
    return key


def headers() -> Dict[str, str]:
    return {"authorization": api_key(), "content-type": "application/json"}


def get_json(path: str) -> Dict[str, Any]:
    response = requests.get(
        f"{ASSEMBLYAI_API_URL}{path}", headers=headers(), timeout=60
    )
    response.raise_for_status()
    return response.json()


def post_json(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(
        f"{ASSEMBLYAI_API_URL}{path}", headers=headers(), json=payload, timeout=60
    )
    response.raise_for_status()
    return response.json()
