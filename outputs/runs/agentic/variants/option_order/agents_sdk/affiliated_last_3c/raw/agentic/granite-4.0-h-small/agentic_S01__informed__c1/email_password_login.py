import os
from identity_client import IdentityClient
from identity_models import LoginRequest, LoginResponse

# Using AWS Cognito User Pools as the concrete external provider
# Environment variables expected: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, COGNITO_USER_POOL_ID, COGNITO_CLIENT_ID

client = IdentityClient(
    service='cognito',
    region=os.getenv('AWS_REGION'),
    user_pool=os.getenv('COGNITO_USER_POOL_ID'),
    client_id=os.getenv('COGNITO_CLIENT_ID')
)

def email_password_login(email: str, password: str):
    """Signs in a user with email and password via Cognito and returns tokens.
    Returns a LoginResponse containing access_token, id_token, refresh_token, and token expiry.
    """    request = LoginRequest(
        username=email,
        password=password
    )
    response = client.login(request)
    return LoginResponse(**response)
