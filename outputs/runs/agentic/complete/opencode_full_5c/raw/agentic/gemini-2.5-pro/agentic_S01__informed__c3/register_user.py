from firebase_admin import auth
from identity_models import UserRegistration
from identity_client import initialize_firebase_app


def create_user(user_data: UserRegistration) -> str:
    """
    Creates a new user in Firebase Authentication.
    """
    initialize_firebase_app()
    try:
        user = auth.create_user(
            email=user_data.email, password=user_data.password, email_verified=False
        )
        return user.uid
    except Exception as e:
        # Error handling for user already exists, weak password etc.
        raise e
