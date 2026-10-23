import os
from typing import Any, Dict

import requests

from identity_client import get_config, verify_google_identity
from identity_models import AccountCredentials, normalize_email, normalize_locale


def register_user(email: str, password: str, google_credential: str, locale: str = "en") -> Dict[str, Any]:
    config = get_config()
    claims = verify_google_identity(google_credential)
    normalized_email = normalize_email(email or claims.get("email", ""))
    payload = {
        "email": normalized_email,
        "password": password,
        "returnSecureToken": True,
        "locale": normalize_locale(locale or claims.get("locale") or config["default_locale"]),
    }
    response = requests.post(
        f'{config["google_identity_toolkit_url"]}/accounts:signUp?key={config["google_api_key"]}',
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
