from identity_client import Auth0Client
from identity_models import UserRegistrationRequest, UserProfile
import logging

logging.basicConfig(level=logging.INFO)


def register_user(request: UserRegistrationRequest) -> UserProfile:
    """
    Registers a new user account with email and password using Auth0 Management API.
    """
    client = Auth0Client()
    management_api = client.get_management_api_client()

    try:
        user_data = management_api.users.create(
            {
                "email": request.email,
                "password": request.password,
                "connection": request.connection,
                "email_verified": False,  # New users typically not verified initially
            }
        )
        logging.info(f"User {request.email} registered successfully with Auth0.")
        return UserProfile(
            user_id=user_data["user_id"],
            email=user_data["email"],
            nickname=user_data.get("nickname"),
            name=user_data.get("name"),
            picture=user_data.get("picture"),
            updated_at=user_data.get("updated_at"),
        )
    except Exception as e:
        logging.error(f"Failed to register user {request.email}: {e}")
        raise
