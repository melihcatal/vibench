from __future__ import annotations

from identity_client import get_identity_client
from identity_models import EmailPasswordIdentityRequest


def email_password_login(email: str, password: str):
    client = get_identity_client()
    request = EmailPasswordIdentityRequest(email=email, password=password)
    return client.login(request)
