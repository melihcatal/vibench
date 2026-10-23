from identity_client import firebase_auth
from identity_models import UserRegistrationRequest, UserRegistrationResponse


def register_user(request: UserRegistrationRequest) -> UserRegistrationResponse:
    """
    Creates a new email/password user account using Firebase Authentication.
    """
    try:
        user = firebase_auth.create_user(email=request.email, password=request.password)
        return UserRegistrationResponse(uid=user.uid)
    except Exception as e:
        # In a real application, you would handle specific Firebase exceptions
        # e.g., auth.EmailAlreadyExistsError
        raise RuntimeError(f"Failed to register user: {e}")
