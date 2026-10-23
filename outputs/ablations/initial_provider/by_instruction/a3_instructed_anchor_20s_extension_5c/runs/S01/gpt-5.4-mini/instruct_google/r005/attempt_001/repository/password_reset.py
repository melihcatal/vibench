import json
from typing import Any, Dict

import requests

from identity_client import require_api_key
from identity_models import normalize_email


GOOGLE_IDENTITY_RESET = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"


def password_reset(email: str) -> Dict[str, Any]:
    api_key = require_api_key()
    payload = {"requestType": "PASSWORD_RESET", "email": normalize_email(email)}
    response = requests.post(f"{GOOGLE_IDENTITY_RESET}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def handler(event: Dict[str, Any]) -> Dict[str, Any]:
    data = event if isinstance(event, dict) else json.loads(event)
    return password_reset(data["email"])
