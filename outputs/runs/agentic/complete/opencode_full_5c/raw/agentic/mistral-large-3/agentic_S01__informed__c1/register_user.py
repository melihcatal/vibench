from typing import Dict, Any
import os
from firebase_admin import auth, initialize_app
from firebase_admin.exceptions import FirebaseError
from identity_models import (
    RegisterUserRequest,
    RegisterUserResponse,
    normalize_firebase_error,
)

# Initialize Firebase Admin SDK with provider-specific credentials
if not auth._apps:
    initialize_app(options={"projectId": os.getenv("FIREBASE_PROJECT_ID")})


def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    """
    Registers a new user with email and password using Firebase Authentication.
    """
    try:
        user = auth.create_user(
            email=request.email,
            password=request.password,
            display_name=request.display_name,
        )
        return RegisterUserResponse(
            success=True, user_id=user.uid, email_verified=user.email_verified
        )
    except FirebaseError as e:
        return RegisterUserResponse(success=False, error=normalize_firebase_error(e))
