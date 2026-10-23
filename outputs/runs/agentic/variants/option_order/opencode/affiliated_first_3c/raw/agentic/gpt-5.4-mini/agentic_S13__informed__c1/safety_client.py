import os
from typing import Any, Dict

import requests


def get_endpoint() -> str:
    return os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "").rstrip("/")


def get_key() -> str:
    return os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")


def post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    endpoint = get_endpoint()
    headers = {
        "Ocp-Apim-Subscription-Key": get_key(),
        "Content-Type": "application/json",
    }
    response = requests.post(
        f"{endpoint}{path}", json=payload, headers=headers, timeout=30
    )
    response.raise_for_status()
    return response.json()
