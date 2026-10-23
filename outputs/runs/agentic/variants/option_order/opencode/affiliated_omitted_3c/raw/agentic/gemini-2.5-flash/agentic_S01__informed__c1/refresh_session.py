import os
from identity_client import Auth0Client
from identity_models import RefreshTokenRequest, RefreshTokenResponse


def refresh_session(refresh_token: str) -> RefreshTokenResponse:
    """Refreshes an expired session or access token using Auth0."""
    client = Auth0Client()
    request = RefreshTokenRequest(
        grant_type="refresh_token",
        client_id=client.client_id,
        refresh_token=refresh_token,
    )
    response = client.refresh_access_token(request)
    return response
