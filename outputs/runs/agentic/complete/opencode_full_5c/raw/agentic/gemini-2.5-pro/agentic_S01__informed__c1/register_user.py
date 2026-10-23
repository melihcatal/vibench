from firebase_admin import auth
from identity_client import initialize_firebase
from identity_models import UserRecord

initialize_firebase()


def register_new_user(email: str, password: str, display_name: str) -> UserRecord:
    """
    Creates a new user in Firebase Authentication.
    """
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name,
        )
        return UserRecord(
            uid=user.uid, email=user.email, display_name=user.display_name
        )
    except Exception as e:
        # In a real application, more specific exception handling is needed
        raise e
