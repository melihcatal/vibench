from __future__ import annotations

from identity_client import Auth0IdentityClient
from identity_models import RefreshRequest


def refresh_session(refresh_token: str):
    request = RefreshRequest(refresh_token=refresh_token)
    client = Auth0IdentityClient()
    tokens = client.refresh(request.refresh_token)
    return {
        "access_token": tokens.access_token,
        "refresh_token": tokens.refresh_token,
        "id_token": tokens.id_token,
        "expires_in": tokens.expires_in,
        "provider": "auth0",
        "raw": tokens.raw,
    }
