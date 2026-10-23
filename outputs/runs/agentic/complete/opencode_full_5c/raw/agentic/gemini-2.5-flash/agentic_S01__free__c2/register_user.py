import firebase_admin
from firebase_admin import credentials, auth
import os

from identity_models import RegisterUserRequest, RegisterUserResponse

# Initialize Firebase Admin SDK if not already initialized
# This assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)


def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    """
    Creates a new email/password user account using Firebase Admin SDK.
    """
    try:
        user = auth.create_user(
            email=request.email,
            password=request.password,
            display_name=request.display_name,
        )
        return RegisterUserResponse(
            uid=user.uid, email=user.email, display_name=user.display_name
        )
    except Exception as e:
        # In a real application, you'd handle different Firebase exceptions
        # (e.g., email-already-exists) more gracefully.
        raise ValueError(f"Failed to register user: {e}")
