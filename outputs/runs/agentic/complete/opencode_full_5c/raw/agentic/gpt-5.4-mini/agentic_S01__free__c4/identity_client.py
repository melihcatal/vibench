import os
from typing import Any, Dict

import requests

from identity_models import normalize_email, normalize_locale


def get_base_url() -> str:
    return os.getenv(
        "IDENTITY_API_BASE_URL", "https://identitytoolkit.googleapis.com/v1"
    )


def get_api_key() -> str:
    return os.getenv("FIREBASE_WEB_API_KEY", os.getenv("IDENTITY_API_KEY", ""))


def request_json(method: str, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{get_base_url().rstrip('/')}/{path.lstrip('/')}"
    params = {"key": get_api_key()} if get_api_key() else {}
    response = requests.request(
        method,
        url,
        params=params,
        json=payload,
        timeout=float(os.getenv("HTTP_TIMEOUT", "20")),
    )
    response.raise_for_status()
    return response.json()


def account_payload(
    email: str, password: str, locale: str = "en", name: str = ""
) -> Dict[str, Any]:
    return {
        "email": normalize_email(email),
        "password": password,
        "returnSecureToken": True,
        "locale": normalize_locale(locale),
        "displayName": name,
    }
