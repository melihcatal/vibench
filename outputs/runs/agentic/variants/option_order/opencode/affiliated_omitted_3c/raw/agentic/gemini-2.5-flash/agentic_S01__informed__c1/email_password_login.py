import os
from identity_client import Auth0Client
from identity_models import LoginRequest, LoginResponse


def email_password_login(email: str, password: str) -> LoginResponse:
    """Signs in a user with email and password using Auth0 and returns tokens."""
    client = Auth0Client()
    # For login, the client_id is usually the application client ID
    # and audience is the identifier of the API you want to access.
    request = LoginRequest(
        username=email,
        password=password,
        client_id=client.client_id,  # This is the application client ID
        audience=client.audience,  # This is the API audience
        scope="openid profile email offline_access",
    )
    response = client.login_user(request)
    return response
