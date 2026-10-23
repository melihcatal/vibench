from __future__ import annotations

from identity_client import Auth0Client, load_auth0_settings
from identity_models import RefreshSessionRequest, TokenResponse


def refresh_session(refresh_token: str) -> dict:
    settings = load_auth0_settings()
    client = Auth0Client(settings=settings)
    request = RefreshSessionRequest(refresh_token=refresh_token)
    payload = client.refresh_token(request.to_refresh_payload(settings.client_id, settings.client_secret))
    return TokenResponse.from_auth0(payload).to_dict()
