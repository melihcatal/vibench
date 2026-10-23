# Refreshes an expired session or access token using Auth0

from identity_client import Auth0IdentityClient
from identity_models import RefreshSessionRequest


def refresh_session(refresh_token: str) -> dict:
    """
    Refresh an expired access token using a refresh token.
    Uses Auth0 OAuth token endpoint.
    """
    client = Auth0IdentityClient()
    request = RefreshSessionRequest(refresh_token=refresh_token)
    response = client.refresh_session(request)
    return response.dict()