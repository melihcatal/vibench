# register_user.py
from identity_client import initialize_firebase_admin
from identity_models import UserRegistrationRequest, User
from firebase_admin.auth import EmailAlreadyExistsError

def create_user_account(registration_request: UserRegistrationRequest) -> User:
    """
    Creates a new user account using Firebase Authentication.
    """
    auth = initialize_firebase_admin()
    try:
        user_record = auth.create_user(
            email=registration_request.email,
            password=registration_request.password,
            display_name=registration_request.display_name,
            email_verified=False  # Typically verification is a separate step
        )
        return User(
            uid=user_record.uid,
            email=user_record.email,
            display_name=user_record.display_name
        )
    except EmailAlreadyExistsError as e:
        print(f"Error: Email {registration_request.email} already exists.")
        raise e
    except Exception as e:
        print(f"An unexpected error occurred during user creation: {e}")
        raise e
