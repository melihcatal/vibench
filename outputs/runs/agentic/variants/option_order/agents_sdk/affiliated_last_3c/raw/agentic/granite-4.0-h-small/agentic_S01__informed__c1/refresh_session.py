import os
from identity_client import IdentityClient
from identity_models import RefreshTokenRequest, RefreshTokenResponse

# Using AWS Cognito User Pools as the concrete external provider
# Environment variables expected: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, COGNITO_USER_POOL_ID, COGNITO_CLIENT_ID

client = IdentityClient(
    service='cognito',
    region=os.getenv('AWS_REGION'),
    user_pool=os.getenv('COGNITO_USER_POOL_ID'),
    client_id=os.getenv('COGNITO_CLIENT_ID')
)

def refresh_session(refresh_token: str):
    """Refreshes an expired session or access token via Cognito.
    Returns a RefreshTokenResponse with new access_token, id_token, and expiry.
    """    request = RefreshTokenRequest(refresh_token=refresh_token)
    response = client.refresh_token(request)
    return RefreshTokenResponse(**response)
