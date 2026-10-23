# Starts a password reset flow for a local account using Auth0

from identity_client import Auth0IdentityClient
from identity_models import PasswordResetRequest


def initiate_password_reset(email: str) -> dict:
    """
    Initiate a password reset flow for a user.
    Uses Auth0 Database Authentication API.
    """
    client = Auth0IdentityClient()
    request = PasswordResetRequest(email=email)
    response = client.initiate_password_reset(request)
    return response.dict()