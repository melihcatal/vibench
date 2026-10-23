from __future__ import annotations

import requests

from identity_client import get_auth0_settings
from identity_models import LoginRequest, TokenResponse


def email_password_login(request: LoginRequest) -> TokenResponse:
    settings = get_auth0_settings()
    payload = request.to_auth0_payload(settings["client_id"], settings["client_secret"])
    if not payload.get("audience") and settings.get("audience"):
        payload["audience"] = settings["audience"]
    response = requests.post(
        f"https://{settings['domain']}/oauth/token",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return TokenResponse.from_auth0(response.json())
