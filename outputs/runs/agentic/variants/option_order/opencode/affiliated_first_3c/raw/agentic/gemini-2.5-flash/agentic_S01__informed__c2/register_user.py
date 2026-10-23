import os
from firebase_admin import auth
from identity_client import initialize_firebase
from identity_models import RegisterUserRequest, RegisterUserResponse

# Initialize Firebase Admin SDK (if not already initialized)
initialize_firebase()


def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    """Creates a new email/password user account using Firebase Authentication."""
    try:
        user = auth.create_user(email=request.email, password=request.password)
        return RegisterUserResponse(uid=user.uid, email=user.email)
    except Exception as e:
        raise ValueError(f"Failed to register user: {e}")
