from __future__ import annotations

from identity_client import IdentityClient
from identity_models import PasswordResetRequest


def password_reset(email: str):
    client = IdentityClient()
    return client.password_reset(PasswordResetRequest(email=email))
