import os
from identity_client import Auth0Client
from identity_models import PasswordResetRequest, PasswordResetResponse


def start_password_reset_flow(
    email: str, connection: str = "Username-Password-Authentication"
) -> PasswordResetResponse:
    """Starts a password reset flow for a local account using Auth0."""
    client = Auth0Client()
    request = PasswordResetRequest(
        email=email, connection=connection, client_id=client.client_id
    )
    response = client.start_password_reset(request)
    return response
