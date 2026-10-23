from __future__ import annotations

from identity_client import IdentityClient


def email_password_login(email: str, password: str):
    client = IdentityClient()
    return client.login(email=email, password=password)
