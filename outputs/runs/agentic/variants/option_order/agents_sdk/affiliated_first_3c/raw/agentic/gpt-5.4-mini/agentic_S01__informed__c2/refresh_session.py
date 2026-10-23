from __future__ import annotations

from identity_client import Auth0IdentityClient
from identity_models import AuthTokens

# Auth0 token refresh integration

def refresh_session(refresh_token: str) -> AuthTokens:
    client = Auth0IdentityClient()
    return client.refresh_session(refresh_token=refresh_token)
