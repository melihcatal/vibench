from __future__ import annotations

from identity_client import Auth0Client
from identity_models import TokenResponse


def refresh_session(refresh_token: str) -> TokenResponse:
    client = Auth0Client()
    data = client.token(
        {
            "grant_type": "refresh_token",
            "client_id": client.config.auth0_client_id,
            "refresh_token": refresh_token,
        }
    )
    return TokenResponse.from_dict(data)
