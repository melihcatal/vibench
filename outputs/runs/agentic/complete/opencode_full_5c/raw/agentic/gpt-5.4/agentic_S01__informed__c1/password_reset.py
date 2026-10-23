from __future__ import annotations

from identity_client import Auth0Client, Auth0Config
from identity_models import PasswordResetRequest


def password_reset(email: str) -> dict:
    config = Auth0Config()
    request = PasswordResetRequest(email=email, connection=config.connection)
    client = Auth0Client(config)
    return client.start_password_reset(request.email, request.connection)
