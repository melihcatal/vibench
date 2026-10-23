from typing import Any, Dict

import requests

from identity_client import get_config
from identity_models import normalize_email


def password_reset(email: str) -> Dict[str, Any]:
    config = get_config()
    response = requests.post(
        f'{config["google_identity_toolkit_url"]}/accounts:sendOobCode?key={config["google_api_key"]}',
        json={"requestType": "PASSWORD_RESET", "email": normalize_email(email)},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
