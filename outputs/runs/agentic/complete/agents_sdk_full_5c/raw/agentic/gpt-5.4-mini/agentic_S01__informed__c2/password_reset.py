from __future__ import annotations

from typing import Any, Dict

from identity_client import get_client
from identity_models import PasswordResetRequest, normalize_email


def password_reset(request: PasswordResetRequest | Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(request, dict):
        request = PasswordResetRequest(**request)
    client = get_client()
    payload = {
        "client_id": client.config.auth0_client_id,
        "email": normalize_email(request.email),
        "connection": "Username-Password-Authentication",
    }
    if request.redirect_url:
        payload["result_url"] = request.redirect_url
    return client.management_request("POST", "/dbconnections/change_password", access_token=client.token("client_credentials", audience=client.config.management_audience)["access_token"], json=payload)
