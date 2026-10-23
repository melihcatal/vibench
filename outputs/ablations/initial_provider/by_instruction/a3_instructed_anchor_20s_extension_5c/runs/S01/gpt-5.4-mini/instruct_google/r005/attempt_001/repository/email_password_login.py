import json
from typing import Any, Dict

import requests

from identity_client import require_api_key
from identity_models import normalize_email, TokenResponse


GOOGLE_IDENTITY_LOGIN = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"


def email_password_login(email: str, password: str) -> TokenResponse:
    api_key = require_api_key()
    payload = {"email": normalize_email(email), "password": password, "returnSecureToken": True}
    response = requests.post(f"{GOOGLE_IDENTITY_LOGIN}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    return TokenResponse.from_dict(response.json())


def handler(event: Dict[str, Any]) -> Dict[str, Any]:
    data = event if isinstance(event, dict) else json.loads(event)
    return email_password_login(data["email"], data["password"]).__dict__
