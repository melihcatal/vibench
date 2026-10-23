from __future__ import annotations

from typing import Any, Dict

from identity_client import get_identity_client
from identity_models import PasswordResetRequest


def password_reset(email: str, redirect_url: str | None = None) -> Dict[str, Any]:
    client = get_identity_client()
    payload = PasswordResetRequest(email=email, redirect_url=redirect_url).payload()
    body = {
        "client_id": client.client_id,
        "email": payload["email"],
        "connection": client.connection,
    }
    if "redirect_url" in payload:
        body["result_url"] = payload["redirect_url"]
    data = client.auth0_request("POST", "/dbconnections/change_password", json=body)
    return client.result(True, data).as_dict()
