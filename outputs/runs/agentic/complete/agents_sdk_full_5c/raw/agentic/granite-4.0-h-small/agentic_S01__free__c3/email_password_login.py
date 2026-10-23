import os
from identity_client import IdentityClient
from identity_models import LoginRequest, LoginResponse


def email_password_login(email: str, password: str) -> LoginResponse:
    """Sign in with email and password.

    Returns tokens (access_token, refresh_token) from the provider.
    """
    client = IdentityClient()
    payload = LoginRequest(email=email, password=password)
    response = client.login_email_password(payload)
    return response