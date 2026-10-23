from __future__ import annotations

from identity_client import Auth0Client
from identity_models import IdentityUser, RegisterUserRequest


def register_user(email: str, password: str, display_name: str | None = None) -> dict:
    client = Auth0Client()
    request = RegisterUserRequest(email=email, password=password, display_name=display_name)
    payload = client.create_db_user(request.to_identity_payload())
    return IdentityUser.from_auth0(payload).to_dict()
