from typing import Any, Dict

import requests

from identity_client import get_config
from identity_models import normalize_email


def email_password_login(email: str, password: str) -> Dict[str, Any]:
    config = get_config()
    response = requests.post(
        f'{config["google_identity_toolkit_url"]}/accounts:signInWithPassword?key={config["google_api_key"]}',
        json={"email": normalize_email(email), "password": password, "returnSecureToken": True},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
