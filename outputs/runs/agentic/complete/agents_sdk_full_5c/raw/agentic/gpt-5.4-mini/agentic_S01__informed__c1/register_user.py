from __future__ import annotations

from identity_client import IdentityClient
from identity_models import RegisterUserRequest


def register_user(email: str, password: str, display_name: str | None = None):
    client = IdentityClient()
    return client.register_user(RegisterUserRequest(email=email, password=password, display_name=display_name))
