import os
from identity_client import Auth0IdentityClient
from identity_models import TokenRefreshRequest, normalize_refresh_response


def refresh_session(refresh_token: str) -> dict:
    client = Auth0IdentityClient()
    request = TokenRefreshRequest(refresh_token=refresh_token)
    response = client.refresh_token(request.refresh_token)
    return normalize_refresh_response(response).dict()
