from __future__ import annotations

from identity_client import IdentityClient
from identity_models import LoginRequest


def email_password_login(email: str, password: str):
    client = IdentityClient()
    return client.login(LoginRequest(email=email, password=password))
