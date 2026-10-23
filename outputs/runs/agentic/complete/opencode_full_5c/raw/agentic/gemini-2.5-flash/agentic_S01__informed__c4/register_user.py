import os
import requests
from identity_client import auth0_client
from identity_models import UserRegistrationRequest, UserProfile


def register_user(request: UserRegistrationRequest) -> UserProfile:
    """Creates a new email/password user account using Auth0 Management API."""
    try:
        user_data = auth0_client.management_client.users.create(
            {
                "email": request.email,
                "password": request.password,
                "connection": request.connection,
                "email_verified": False,  # Typically email verification happens after registration
            }
        )
        return UserProfile(
            user_id=user_data["user_id"],
            email=user_data["email"],
            email_verified=user_data["email_verified"],
            created_at=user_data["created_at"],
            updated_at=user_data["updated_at"],
            name=user_data.get("name"),
            picture=user_data.get("picture"),
        )
    except Exception as e:
        raise RuntimeError(f"Auth0 user registration failed: {e}")
