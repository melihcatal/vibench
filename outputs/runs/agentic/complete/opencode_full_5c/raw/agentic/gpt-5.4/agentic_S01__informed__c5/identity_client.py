from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests
from openai import OpenAI
from pymongo import MongoClient


class IdentityConfigurationError(ValueError):
    pass


def _get_env(name: str, default: Optional[str] = None, required: bool = True) -> str:
    value = os.getenv(name, default)
    if required and not value:
        raise IdentityConfigurationError(
            f"Missing required environment variable: {name}"
        )
    return value or ""


def get_auth0_settings() -> Dict[str, str]:
    domain = _get_env("AUTH0_DOMAIN")
    return {
        "domain": domain,
        "client_id": _get_env("AUTH0_CLIENT_ID"),
        "client_secret": _get_env("AUTH0_CLIENT_SECRET"),
        "connection": _get_env(
            "AUTH0_DB_CONNECTION",
            default="Username-Password-Authentication",
            required=False,
        )
        or "Username-Password-Authentication",
        "audience": os.getenv("AUTH0_AUDIENCE", ""),
        "management_audience": f"https://{domain}/api/v2/",
    }


def get_auth0_management_token() -> str:
    settings = get_auth0_settings()
    response = requests.post(
        f"https://{settings['domain']}/oauth/token",
        json={
            "grant_type": "client_credentials",
            "client_id": settings["client_id"],
            "client_secret": settings["client_secret"],
            "audience": settings["management_audience"],
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def auth0_headers(token: Optional[str] = None) -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def get_deepl_settings() -> Dict[str, str]:
    return {
        "auth_key": _get_env("DEEPL_AUTH_KEY"),
        "api_url": os.getenv("DEEPL_API_URL", "https://api.deepl.com/v2/translate"),
    }


def get_perspective_settings() -> Dict[str, str]:
    return {
        "api_key": _get_env("PERSPECTIVE_API_KEY"),
        "api_url": "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
    }


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=_get_env("OPENAI_API_KEY"))


def get_mongodb_collection():
    uri = _get_env("MONGODB_ATLAS_URI")
    database_name = _get_env("MONGODB_ATLAS_DATABASE")
    collection_name = _get_env("MONGODB_ATLAS_COLLECTION")
    client = MongoClient(uri)
    return client[database_name][collection_name]


def normalize_locale(locale: str) -> str:
    normalized = locale.replace("_", "-").strip()
    if not normalized:
        raise ValueError("locale must not be empty")
    return normalized


def compact_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}
