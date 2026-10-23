from __future__ import annotations

from identity_client import Auth0IdentityClient
from identity_models import PasswordResetRequest


def password_reset(email: str):
    client = Auth0IdentityClient()
    return client.start_password_reset(PasswordResetRequest(email=email))
