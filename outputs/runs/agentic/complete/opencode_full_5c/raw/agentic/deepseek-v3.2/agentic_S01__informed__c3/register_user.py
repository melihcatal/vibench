import os
from identity_client import get_auth0_client


def register_user(email: str, password: str, user_metadata: dict = None) -> dict:
    """Create a new email/password user account using Auth0."""
    client = get_auth0_client()

    user_data = {
        "email": email,
        "password": password,
        "connection": "Username-Password-Authentication",
        "email_verified": False,
    }

    if user_metadata:
        user_data["user_metadata"] = user_metadata

    try:
        response = client.users.create(user_data)
        return {
            "user_id": response["user_id"],
            "email": response["email"],
            "email_verified": response.get("email_verified", False),
            "created_at": response.get("created_at"),
        }
    except Exception as e:
        raise Exception(f"Failed to register user with Auth0: {str(e)}")
