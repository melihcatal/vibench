import os
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from identity_models import RegisterUserRequest, RegisterUserResponse

# Firebase project ID can be set via GOOGLE_CLOUD_PROJECT environment variable
# or explicitly initialized.
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    try:
        user = auth.create_user(
            email=request.email,
            password=request.password,
            display_name=request.display_name
        )
        return RegisterUserResponse(
            uid=user.uid,
            email=user.email,
            display_name=user.display_name
        )
    except Exception as e:
        # In a real application, you'd handle different Firebase Auth exceptions
        # more granularly.
        raise RuntimeError(f"Failed to register user: {e}")
