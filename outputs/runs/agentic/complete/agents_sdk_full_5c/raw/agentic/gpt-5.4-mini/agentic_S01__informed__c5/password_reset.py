from __future__ import annotations

from identity_client import IdentityClient
from identity_models import PasswordResetRequest


def password_reset(email: str, locale: str | None = None):
    client = IdentityClient()
    request = PasswordResetRequest(email=email, locale=locale)
    return client.password_reset(request)
