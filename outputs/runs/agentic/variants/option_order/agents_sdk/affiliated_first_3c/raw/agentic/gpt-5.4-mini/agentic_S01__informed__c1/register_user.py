from __future__ import annotations

from identity_client import Auth0IdentityClient
from identity_models import RegisterRequest


def register_user(email: str, password: str, display_name: str | None = None, locale: str = "en", metadata: dict | None = None):
    request = RegisterRequest(
        email=email,
        password=password,
        display_name=display_name,
        locale=locale,
        metadata=metadata or {},
    )
    client = Auth0IdentityClient()
    user = client.create_user(
        email=request.normalized()["email"],
        password=request.password,
        display_name=request.normalized()["display_name"],
        metadata=request.normalized()["metadata"],
    )
    return {
        "user_id": user.user_id,
        "email": user.email,
        "email_verified": user.email_verified,
        "display_name": user.display_name,
        "provider": "auth0",
        "raw": user.raw,
    }
