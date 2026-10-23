from identity_client import get_firebase_auth_client
from identity_models import UserRegistration
from firebase_admin.auth import UserRecord

def create_user_account(user_data: UserRegistration) -> UserRecord:
    """
    Creates a new user account using Firebase Authentication.

    Args:
        user_data: An object containing user registration details.

    Returns:
        The newly created user record from Firebase.
    """
    auth_client = get_firebase_auth_client()
    try:
        user = auth_client.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.display_name,
            email_verified=False
        )
        print(f"Successfully created new user: {user.uid}")
        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        raise
