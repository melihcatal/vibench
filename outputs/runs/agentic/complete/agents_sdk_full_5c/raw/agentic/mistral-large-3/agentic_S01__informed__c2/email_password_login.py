# Signs in a user with email and password and returns tokens using Auth0

from identity_client import Auth0IdentityClient
from identity_models import LoginRequest


def email_password_login(email: str, password: str) -> dict:
    """
    Authenticate a user with email and password.
    Uses Auth0 Database Authentication API.
    """
    client = Auth0IdentityClient()
    request = LoginRequest(email=email, password=password)
    response = client.login(request)
    return response.dict()