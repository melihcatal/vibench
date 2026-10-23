import firebase_admin
from firebase_admin import auth
from identity_client import initialize_firebase_admin
from identity_models import UserRegistrationRequest, UserRegistrationResponse

initialize_firebase_admin()

def create_user(registration_request: UserRegistrationRequest) -> UserRegistrationResponse:
    """
    Creates a new user in Firebase Authentication.
    """
    try:
        user = auth.create_user(
            email=registration_request.email,
            password=registration_request.password,
            display_name=registration_request.display_name,
            email_verified=False
        )
        return UserRegistrationResponse(
            uid=user.uid,
            email=user.email,
            display_name=user.display_name
        )
    except firebase_admin.auth.EmailAlreadyExistsError as e:
        raise ValueError(f"Email already exists: {registration_request.email}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to create user: {e}") from e
