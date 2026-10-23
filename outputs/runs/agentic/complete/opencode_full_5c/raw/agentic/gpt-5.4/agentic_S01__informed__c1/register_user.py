from __future__ import annotations

from identity_client import Auth0Client, Auth0Config
from identity_models import IdentityUser, RegisterUserRequest


def register_user(
    email: str,
    password: str,
    given_name: str | None = None,
    family_name: str | None = None,
) -> IdentityUser:
    config = Auth0Config()
    request = RegisterUserRequest(
        email=email,
        password=password,
        given_name=given_name,
        family_name=family_name,
        connection=config.connection,
    )
    client = Auth0Client(config)
    created_user = client.create_database_user(request.to_auth0_payload())
    return IdentityUser.from_auth0_user(created_user)
