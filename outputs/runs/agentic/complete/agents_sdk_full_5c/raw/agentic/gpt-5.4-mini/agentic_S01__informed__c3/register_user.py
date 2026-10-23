from __future__ import annotations

from typing import Any, Dict

from identity_client import get_identity_client
from identity_models import EmailPasswordRegistration


def register_user(email: str, password: str, locale: str = "en", display_name: str | None = None) -> Dict[str, Any]:
    client = get_identity_client()
    payload = EmailPasswordRegistration(email=email, password=password, locale=locale, display_name=display_name).payload()
    body = {
        "email": payload["email"],
        "password": payload["password"],
        "connection": client.connection,
        "user_metadata": {"locale": payload["locale"], "display_name": payload["display_name"]},
    }
    data = client.auth0_request("POST", "/api/v2/users", json=body)
    return client.result(True, data).as_dict()
