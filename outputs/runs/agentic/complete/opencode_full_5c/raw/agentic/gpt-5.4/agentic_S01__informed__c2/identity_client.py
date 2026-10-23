from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


class IdentityConfigurationError(ValueError):
    pass


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise IdentityConfigurationError(
            f"Missing required environment variable: {name}"
        )
    return value


def auth0_domain() -> str:
    return _require_env("AUTH0_DOMAIN")


def auth0_client_id() -> str:
    return _require_env("AUTH0_CLIENT_ID")


def auth0_client_secret() -> Optional[str]:
    return os.getenv("AUTH0_CLIENT_SECRET")


def auth0_audience() -> str:
    return os.getenv("AUTH0_AUDIENCE", f"https://{auth0_domain()}/api/v2/")


def auth0_base_url() -> str:
    return f"https://{auth0_domain()}"


def auth0_db_connection() -> str:
    return os.getenv("AUTH0_DB_CONNECTION", "Username-Password-Authentication")


def auth0_management_token() -> str:
    response = requests.post(
        f"{auth0_base_url()}/oauth/token",
        json={
            "grant_type": "client_credentials",
            "client_id": auth0_client_id(),
            "client_secret": _require_env("AUTH0_CLIENT_SECRET"),
            "audience": auth0_audience(),
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def auth0_headers(bearer_token: Optional[str] = None) -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"
    return headers


def auth0_post(
    path: str, payload: Dict[str, Any], bearer_token: Optional[str] = None
) -> Dict[str, Any]:
    response = requests.post(
        f"{auth0_base_url()}{path}",
        headers=auth0_headers(bearer_token),
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    if response.content:
        return response.json()
    return {}
