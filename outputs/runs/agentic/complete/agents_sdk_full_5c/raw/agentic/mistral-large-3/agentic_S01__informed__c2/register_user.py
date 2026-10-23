# Creates a new email/password user account using Auth0

from identity_client import Auth0IdentityClient
from identity_models import RegisterUserRequest


def register_user(email: str, password: str, given_name: str = None, family_name: str = None, locale: str = None) -> dict:
    """
    Register a new user with email and password.
    Uses Auth0 Management API for user creation.
    """
    client = Auth0IdentityClient()
    request = RegisterUserRequest(
        email=email,
        password=password,
        given_name=given_name,
        family_name=family_name,
        locale=locale
    )
    response = client.register_user(request)
    return response.dict()