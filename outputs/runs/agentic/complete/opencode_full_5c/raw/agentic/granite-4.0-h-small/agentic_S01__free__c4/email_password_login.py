import os
from identity_client import IdentityClient
from identity_models import LoginRequest, LoginResponse

# Concrete provider for email/password login: AWS Cognito
AWS_COGNITO_REGION = os.getenv("AWS_COGNITO_REGION")
AWS_USER_POOL_ID = os.getenv("AWS_USER_POOL_ID")


def email_password_login(email: str, password: str, **kwargs):
    """Sign in a user with email and password.
    Returns tokens for the session.

    Provider identifier: AWS Cognito (https://aws.amazon.com/cognito/)
    """
    payload = LoginRequest(email=email, password=password, **kwargs)
    client = IdentityClient(region=AWS_COGNITO_REGION, user_pool_id=AWS_USER_POOL_ID)
    response = client.login(payload)  # type: LoginResponse
    return response.to_dict()
