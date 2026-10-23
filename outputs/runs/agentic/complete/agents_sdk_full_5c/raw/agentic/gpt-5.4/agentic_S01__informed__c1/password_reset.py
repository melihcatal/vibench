from __future__ import annotations

from typing import Any, Dict

from identity_client import get_auth0_client
from identity_models import PasswordResetRequest


def password_reset(request: PasswordResetRequest) -> Dict[str, Any]:
    client = get_auth0_client()
    payload = request.to_auth0_payload(client.client_id, client.connection)
    client._post("/dbconnections/change_password", payload)
    return {
        "status": "password_reset_requested",
        "provider": "Auth0 Authentication API",
        "email": request.email,
        "connection": client.connection,
    }
