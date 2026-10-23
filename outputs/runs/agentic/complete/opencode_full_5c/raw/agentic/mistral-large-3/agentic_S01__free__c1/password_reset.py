import os
from identity_client import Auth0IdentityClient
from identity_models import PasswordResetRequest


def password_reset(email: str) -> None:
    client = Auth0IdentityClient()
    request = PasswordResetRequest(email=email)
    client.start_password_reset(email=request.email, connection=request.connection)
