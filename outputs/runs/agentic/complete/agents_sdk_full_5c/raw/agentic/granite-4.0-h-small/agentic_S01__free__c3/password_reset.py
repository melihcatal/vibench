import os
from identity_client import IdentityClient
from identity_models import PasswordResetRequest


def start_password_reset(email: str):
    """Initiate a password reset flow for a local account.
    """
    client = IdentityClient()
    payload = PasswordResetRequest(email=email)
    client.start_password_reset(payload)