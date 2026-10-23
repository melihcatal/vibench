from __future__ import annotations

from identity_client import Auth0IdentityClient
from identity_models import PasswordResetRequest


def password_reset(email: str):
    request = PasswordResetRequest(email=email)
    client = Auth0IdentityClient()
    result = client.start_password_reset(request.normalized()["email"])
    result["provider"] = "auth0"
    return result
