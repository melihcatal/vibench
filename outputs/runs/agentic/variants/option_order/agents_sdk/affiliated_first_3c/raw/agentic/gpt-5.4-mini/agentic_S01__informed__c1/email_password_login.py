from __future__ import annotations

from identity_client import Auth0IdentityClient
from identity_models import LoginRequest


def email_password_login(email: str, password: str):
    request = LoginRequest(email=email, password=password)
    client = Auth0IdentityClient()
    tokens = client.password_realm_grant(**request.normalized())
    return {
        "access_token": tokens.access_token,
        "refresh_token": tokens.refresh_token,
        "id_token": tokens.id_token,
        "expires_in": tokens.expires_in,
        "provider": "auth0",
        "raw": tokens.raw,
    }
