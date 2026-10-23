import os
from typing import Any, Dict

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def get_api_key() -> str:
    key = os.getenv("PERSPECTIVE_API_KEY", "")
    if not key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    return key


def build_perspective_payload(
    text: str, languages=None, attributes=None
) -> Dict[str, Any]:
    return {
        "comment": {"text": text},
        "languages": languages or ["en"],
        "requestedAttributes": attributes or {"TOXICITY": {}},
    }


def perspective_headers() -> Dict[str, str]:
    return {"Content-Type": "application/json"}


def post_moderation(payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.get(
        PERSPECTIVE_API_URL,
        params={"key": get_api_key()},
        headers=perspective_headers(),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
