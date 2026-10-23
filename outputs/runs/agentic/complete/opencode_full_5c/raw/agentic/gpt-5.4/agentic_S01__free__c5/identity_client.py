from __future__ import annotations

import os
from typing import Any

import requests


FIREBASE_IDENTITY_TOOLKIT_BASE_URL = "https://identitytoolkit.googleapis.com/v1"
FIREBASE_SECURE_TOKEN_URL = "https://securetoken.googleapis.com/v1/token"


class FirebaseIdentityError(Exception):
    pass


def get_firebase_api_key() -> str:
    api_key = os.environ.get("FIREBASE_WEB_API_KEY") or os.environ.get(
        "FIREBASE_API_KEY"
    )
    if not api_key:
        raise FirebaseIdentityError("Missing FIREBASE_WEB_API_KEY or FIREBASE_API_KEY")
    return api_key


def get_identity_timeout() -> float:
    raw = os.environ.get("FIREBASE_AUTH_TIMEOUT_SECONDS", "30")
    return float(raw)


def firebase_auth_headers() -> dict[str, str]:
    return {"Content-Type": "application/json"}


def firebase_identity_url(path: str) -> str:
    return f"{FIREBASE_IDENTITY_TOOLKIT_BASE_URL}/{path}?key={get_firebase_api_key()}"


def post_json(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(
        url,
        json=payload,
        headers=firebase_auth_headers(),
        timeout=get_identity_timeout(),
    )
    response.raise_for_status()
    return response.json()


def post_form(url: str, data: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(url, data=data, timeout=get_identity_timeout())
    response.raise_for_status()
    return response.json()
