from __future__ import annotations

from identity_client import get_identity_client
from identity_models import EmailPasswordIdentityRequest


def password_reset(email: str):
    client = get_identity_client()
    request = EmailPasswordIdentityRequest(email=email)
    return client.password_reset(request)
