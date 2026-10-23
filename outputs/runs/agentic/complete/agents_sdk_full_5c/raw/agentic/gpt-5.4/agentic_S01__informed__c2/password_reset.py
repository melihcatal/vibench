from __future__ import annotations

from typing import Any, Dict

from identity_client import Auth0Client
from identity_models import PasswordResetRequest


def password_reset(request: PasswordResetRequest) -> Dict[str, Any]:
    client = Auth0Client()
    payload = request.to_auth0_payload(client.client_id)
    data = client.start_password_reset(payload)
    return {"status": "password_reset_requested", "provider": "Auth0", "response": data}


def password_reset_from_dict(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = PasswordResetRequest(**payload)
    return password_reset(request)
