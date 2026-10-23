from __future__ import annotations

from typing import Any, Dict

import requests

from identity_client import get_identity_client
from identity_models import EmailPasswordLoginRequest


def email_password_login(email: str, password: str) -> Dict[str, Any]:
    client = get_identity_client()
    payload = EmailPasswordLoginRequest(email=email, password=password).payload()
    url = f"https://{client.domain}/oauth/token"
    body = {
        "grant_type": "password",
        "username": payload["email"],
        "password": payload["password"],
        "audience": f"https://{client.domain}/api/v2/",
        "scope": "openid profile email offline_access",
        "client_id": client.client_id,
        "client_secret": client.client_secret,
        "realm": client.connection,
    }
    response = requests.post(url, json=body, headers={"Content-Type": "application/json"}, timeout=30)
    response.raise_for_status()
    return client.result(True, response.json()).as_dict()
