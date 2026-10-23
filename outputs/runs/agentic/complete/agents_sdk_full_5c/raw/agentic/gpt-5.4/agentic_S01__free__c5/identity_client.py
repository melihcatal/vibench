from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


class IdentityClientConfig:
    def __init__(self) -> None:
        self.firebase_web_api_key = os.environ["FIREBASE_WEB_API_KEY"]
        self.firebase_project_id = os.environ.get("FIREBASE_PROJECT_ID", "")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")
        self.deepl_api_key = os.environ.get("DEEPL_API_KEY", "")
        self.firestore_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or self.firebase_project_id


def load_config() -> IdentityClientConfig:
    return IdentityClientConfig()


def firebase_identity_toolkit_url(path: str, api_key: str) -> str:
    return f"https://identitytoolkit.googleapis.com/v1/{path}?key={api_key}"


def firebase_secure_token_url(api_key: str) -> str:
    return f"https://securetoken.googleapis.com/v1/token?key={api_key}"


def require_http_ok(response: requests.Response) -> Dict[str, Any]:
    response.raise_for_status()
    return response.json()


def bearer_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def optional_dict(data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return data or {}
