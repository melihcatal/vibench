import os
from typing import Any, Dict

import requests


OPENAI_IDENTITY_BASE_URL = "https://api.openai.com/v1"


def get_identity_api_key() -> str:
    return os.environ.get("OPENAI_API_KEY", "")


def get_identity_base_url() -> str:
    return os.environ.get("OPENAI_IDENTITY_BASE_URL", OPENAI_IDENTITY_BASE_URL)


def build_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {get_identity_api_key()}",
        "Content-Type": "application/json",
    }


def post_json(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(f"{get_identity_base_url()}{path}", json=payload, headers=build_headers(), timeout=30)
    response.raise_for_status()
    return response.json()
