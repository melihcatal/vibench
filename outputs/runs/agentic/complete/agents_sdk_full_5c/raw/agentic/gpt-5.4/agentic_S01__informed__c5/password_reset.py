from __future__ import annotations

from typing import Any, Dict

from identity_client import get_identity_client
from identity_models import PasswordResetRequest, normalize_email


def password_reset(request: PasswordResetRequest) -> Dict[str, Any]:
    client = get_identity_client()
    payload = {
        "client_id": client.client_id,
        "email": normalize_email(request.email),
        "connection": client.connection,
    }
    response = client.post_json("/dbconnections/change_password", payload)
    return {
        "provider": "auth0",
        "domain": client.domain,
        "email": normalize_email(request.email),
        "message": response if isinstance(response, str) else response.get("message", "password reset started"),
    }
