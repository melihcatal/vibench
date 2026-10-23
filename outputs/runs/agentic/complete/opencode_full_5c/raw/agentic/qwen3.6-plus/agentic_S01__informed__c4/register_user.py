import os
from identity_client import register_user, AUTH0_CONNECTION
from identity_models import RegisterUserRequest, AuthResponse


def create_account(
    email: str,
    password: str,
    given_name: str = "",
    family_name: str = "",
    metadata: dict = None,
) -> AuthResponse:
    auth0_domain = os.environ.get("AUTH0_DOMAIN", "")
    auth0_client_id = os.environ.get("AUTH0_CLIENT_ID", "")
    auth0_client_secret = os.environ.get("AUTH0_CLIENT_SECRET", "")

    if not auth0_domain:
        raise ValueError(
            "AUTH0_DOMAIN environment variable is required for Auth0 user registration"
        )

    req = RegisterUserRequest(
        email=email,
        password=password,
        connection=AUTH0_CONNECTION,
        given_name=given_name or None,
        family_name=family_name or None,
        metadata=metadata,
    )

    result = register_user(req=req)
    return result
