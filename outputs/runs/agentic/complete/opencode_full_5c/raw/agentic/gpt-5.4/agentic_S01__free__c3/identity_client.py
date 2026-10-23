from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def auth0_domain() -> str:
    return _require_env("AUTH0_DOMAIN")


def auth0_client_id() -> str:
    return _require_env("AUTH0_CLIENT_ID")


def auth0_client_secret() -> str:
    return _require_env("AUTH0_CLIENT_SECRET")


def auth0_db_connection() -> str:
    return os.getenv("AUTH0_DB_CONNECTION", "Username-Password-Authentication")


def auth0_audience() -> Optional[str]:
    return os.getenv("AUTH0_AUDIENCE")


def auth0_base_url() -> str:
    domain = auth0_domain().strip().rstrip("/")
    if domain.startswith("https://"):
        return domain
    return f"https://{domain}"


def auth0_post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(
        f"{auth0_base_url()}{path}",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    if not response.content:
        return {}
    return response.json()


def openai_api_key() -> str:
    return _require_env("OPENAI_API_KEY")


def openai_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {openai_api_key()}",
        "Content-Type": "application/json",
    }


def openai_post(payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers=openai_headers(),
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def firestore_project_id() -> str:
    return _require_env("GOOGLE_CLOUD_PROJECT")
