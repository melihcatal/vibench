import os
from identity_client import IdentityClient
from identity_models import UserRegisterRequest, UserRegisterResponse

# Use Amazon Cognito User Pools as the concrete provider
COGNITO_POOL_ID = os.getenv('COGNITO_POOL_ID')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
COGNITO_REGION = os.getenv('COGNITO_REGION', 'us-east-1')

def register_user(email: str, password: str, afd_id: str) -> UserRegisterResponse:
    """Registers a new email/password user account using Amazon Cognito User Pools.

    Returns the registration response.
    """
    request = UserRegisterRequest(
        username=email,  # Cognito uses email as username
        password=password,
        user_attributes={
            'email': email,
            # Add any other required attributes here
        },
    )
    client = IdentityClient(
        service='cognito',
        region=COGNITO_REGION,
        client_id=COGNITO_CLIENT_ID,
        pool_id=COGNITO_POOL_ID,
    )
    response = client.register_user(request)
    return response
