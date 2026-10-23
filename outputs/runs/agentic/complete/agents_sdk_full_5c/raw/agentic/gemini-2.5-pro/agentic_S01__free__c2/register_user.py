from firebase_admin import auth
from identity_client import get_firebase_app
from identity_models import UserCreateRequest, User

def register(user_data: UserCreateRequest) -> User:
    """
    Creates a new user in Firebase Authentication.
    """
    get_firebase_app()  # Ensure Firebase app is initialized

    try:
        user_record = auth.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.display_name,
            email_verified=False, # Default to unverified
        )
        return User(
            uid=user_record.uid,
            email=user_record.email,
            display_name=user_record.display_name
        )
    except Exception as e:
        # In a real app, handle specific Firebase errors
        # (e.g., EMAIL_EXISTS)
        raise e
