from __future__ import annotations

from identity_client import Auth0Client, load_auth0_config
from identity_models import RefreshRequest, TokenResponse


def refresh_session(refresh_token: str) -> dict:
    config = load_auth0_config()
    client = Auth0Client(config)
    request = RefreshRequest(refresh_token=refresh_token)
    response = client.post(
        "/oauth/token",
        request.to_auth0_payload(client_id=config.client_id, client_secret=config.client_secret),
    )
    return TokenResponse.from_auth0(response).to_dict()
