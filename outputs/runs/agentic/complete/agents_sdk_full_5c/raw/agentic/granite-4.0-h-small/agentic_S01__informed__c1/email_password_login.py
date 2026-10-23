import os
from identity_client import IdentityClient
from identity_models import TokenResponse

# Amazon Cognito federated identities as the concrete provider
COGNITO_REGION = os.getenv('COGNITO_REGION', 'us-east-1')
COGNITO_IDENTITY_POOL_ID = os.getenv('COGNITO_IDENTITY_POOL_ID')
COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')


def login(email: str, password: str) -> TokenResponse:
    """Sign in a user with email and password using Amazon Cognito User Pools.

    Returns tokens: access_token, id_token, refresh_token.
    """
    client = IdentityClient(
        service='cognito',
        region=COGNITO_REGION,
        user_pool_id=COGNITO_USER_POOL_ID,
        identity_pool_id=COGNITO_IDENTITY_POOL_ID,
    )
    return client.login(email=email, password=password)
