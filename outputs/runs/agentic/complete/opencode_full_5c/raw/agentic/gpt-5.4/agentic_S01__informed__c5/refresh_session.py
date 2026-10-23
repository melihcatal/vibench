from __future__ import annotations

import requests

from identity_client import get_auth0_settings
from identity_models import RefreshSessionRequest, TokenResponse


def refresh_session(request: RefreshSessionRequest) -> TokenResponse:
    settings = get_auth0_settings()
    response = requests.post(
        f"https://{settings['domain']}/oauth/token",
        json=request.to_auth0_payload(settings["client_id"], settings["client_secret"]),
        timeout=30,
    )
    response.raise_for_status()
    return TokenResponse.from_auth0(response.json())
