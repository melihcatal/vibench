import os
from identity_client import IdentityClient
from identity_models import RegisterRequest, RegisterResponse

# Using AWS Cognito User Pools as the concrete external provider
# Environment variables expected: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, COGNITO_USER_POOL_ID, COGNITO_CLIENT_ID

client = IdentityClient(
    service='cognito',
    region=os.getenv('AWS_REGION'),
    user_pool=os.getenv('COGNITO_USER_POOL_ID'),
    client_id=os.getenv('COGNITO_CLIENT_ID')
)

def register_user(email: str, password: str, **custom_attrs):
    """Creates a new email/password user account via Cognito.
    Returns a RegisterResponse containing user attributes and confirmation state.
    """    request = RegisterRequest(
        username=email,
        password=password,
        user_attributes=[
            {'Name': 'email', 'Value': email},
            # add any additional standard or custom attributes here
        ],
        **custom_attrs
    )
    response = client.register(request)
    return RegisterResponse(**response)
