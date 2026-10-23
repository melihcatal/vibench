import os
from identity_client import Auth0Client
from identity_models import RegisterUserRequest, RegisterUserResponse


def register_user_account(email: str, password: str) -> RegisterUserResponse:
    """Creates a new email/password user account using Auth0."""
    client = Auth0Client()
    request = RegisterUserRequest(email=email, password=password)
    response = client.register_user(request)
    return response
