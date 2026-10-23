from __future__ import annotations

import requests

from identity_client import get_auth0_settings
from identity_models import PasswordResetRequest


def password_reset(request: PasswordResetRequest) -> dict:
    settings = get_auth0_settings()
    response = requests.post(
        f"https://{settings['domain']}/dbconnections/change_password",
        json=request.to_auth0_payload(settings["client_id"], settings["connection"]),
        timeout=30,
    )
    response.raise_for_status()
    return {
        "provider": "auth0",
        "domain": settings["domain"],
        "message": response.text,
    }
