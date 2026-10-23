import os
from identity_client import get_auth0_client
from identity_models import UserRegistrationRequest, UserRegistrationResponse


def register_user(
    email: str, password: str, name: str = None
) -> UserRegistrationResponse:
    """Create a new email/password user account using Auth0."""
    client = get_auth0_client()

    user_data = {
        "email": email,
        "password": password,
        "connection": "Username-Password-Authentication",
        "email_verified": False,
    }

    if name:
        user_data["name"] = name
        user_data["given_name"] = name.split()[0] if " " in name else name

    try:
        response = client.users.create(user_data)

        return UserRegistrationResponse(
            user_id=response["user_id"],
            email=response["email"],
            created_at=response["created_at"],
            provider="auth0",
        )
    except Exception as e:
        raise Exception(f"Failed to register user with Auth0: {str(e)}")
