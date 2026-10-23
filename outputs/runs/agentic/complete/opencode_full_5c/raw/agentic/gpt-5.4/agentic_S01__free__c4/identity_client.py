from __future__ import annotations

import os
from typing import Any

import requests
from google.cloud import firestore


FIREBASE_AUTH_BASE_URL = "https://identitytoolkit.googleapis.com/v1"
FIREBASE_SECURE_TOKEN_URL = "https://securetoken.googleapis.com/v1/token"
DEEPL_API_URL = "https://api.deepl.com/v2/translate"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def firebase_api_key() -> str:
    return require_env("FIREBASE_WEB_API_KEY")


def firebase_auth_url(path: str) -> str:
    return f"{FIREBASE_AUTH_BASE_URL}/{path}?key={firebase_api_key()}"


def firebase_post(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(firebase_auth_url(path), json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def firebase_refresh_token(refresh_token: str) -> dict[str, Any]:
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    response = requests.post(
        f"{FIREBASE_SECURE_TOKEN_URL}?key={firebase_api_key()}",
        data=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def deepl_headers() -> dict[str, str]:
    return {
        "Authorization": f"DeepL-Auth-Key {require_env('DEEPL_API_KEY')}",
        "Content-Type": "application/json",
    }


def openai_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {require_env('OPENAI_API_KEY')}",
        "Content-Type": "application/json",
    }


def openai_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def firestore_client() -> firestore.Client:
    project_id = require_env("GOOGLE_CLOUD_PROJECT")
    return firestore.Client(project=project_id)
