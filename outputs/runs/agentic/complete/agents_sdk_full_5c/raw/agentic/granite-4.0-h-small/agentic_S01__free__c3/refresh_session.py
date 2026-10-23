import os
from identity_client import IdentityClient
from identity_models import RefreshRequest, RefreshResponse


def refresh_session(refresh_token: str) -> RefreshResponse:
    """Refresh an expired access token using the provider's refresh endpoint.

    Returns a new access token and optional new refresh token.
    """
    client = IdentityClient()
    payload = RefreshRequest(refresh_token=refresh_token)
    response = client.refresh_token(payload)
    return response