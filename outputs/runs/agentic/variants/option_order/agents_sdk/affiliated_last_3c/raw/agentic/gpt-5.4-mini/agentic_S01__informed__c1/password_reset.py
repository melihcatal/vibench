from __future__ import annotations

from identity_client import CognitoIdentityClient
from identity_models import PasswordResetRequest


def password_reset(email: str, locale: str | None = None):
    request = PasswordResetRequest(email=email, locale=locale)
    return CognitoIdentityClient().start_password_reset(**request.normalized())
