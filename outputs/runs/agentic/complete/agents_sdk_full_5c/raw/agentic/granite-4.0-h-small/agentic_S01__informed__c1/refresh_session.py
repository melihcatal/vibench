import os
from identity_client import IdentityClient
from identity_models import RefreshSessionRequest, RefreshSessionResponse

# Concrete integration: Amazon Cognito User Pools
COGNITO_REGION = os.getenv('COGNITO_REGION', 'us-east-1')
COGNITO_POOL_ID = os.getenv('COGNITO_POOL_ID')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')


def refresh_session(refresh_token: str) -> RefreshSessionResponse:
    """Refresh an expired session or access token using a refresh token.

    Returns new tokens (access_token, id_token, refresh_token) or raises on failure.
    """
    client = IdentityClient(
        service='cognito',
        region=COGNITO_REGION,
        user_pool_id=COGNITO_POOL_ID,
        client_id=COGNITO_CLIENT_ID,
    )
    return client.refresh_session(refresh_token=refresh_token)
