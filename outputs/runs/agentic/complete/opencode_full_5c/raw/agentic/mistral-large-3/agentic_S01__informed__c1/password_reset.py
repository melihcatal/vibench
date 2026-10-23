from typing import Dict, Any
import os
from firebase_admin import auth, initialize_app
from firebase_admin.exceptions import FirebaseError
from identity_models import (
    PasswordResetRequest,
    PasswordResetResponse,
    normalize_firebase_error,
)

# Initialize Firebase Admin SDK with provider-specific credentials
if not auth._apps:
    initialize_app(options={"projectId": os.getenv("FIREBASE_PROJECT_ID")})


def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    """
    Starts a password reset flow for a user using Firebase Authentication.
    """
    try:
        # Generate a password reset link for the user
        link = auth.generate_password_reset_link(request.email)
        return PasswordResetResponse(success=True, reset_link=link)
    except FirebaseError as e:
        return PasswordResetResponse(success=False, error=normalize_firebase_error(e))
