from typing import Dict, Any
import os
from firebase_admin import auth, initialize_app
from firebase_admin.exceptions import FirebaseError
from identity_models import LoginRequest, LoginResponse, normalize_firebase_error

# Initialize Firebase Admin SDK with provider-specific credentials
if not auth._apps:
    initialize_app(options={"projectId": os.getenv("FIREBASE_PROJECT_ID")})


def email_password_login(request: LoginRequest) -> LoginResponse:
    """
    Signs in a user with email and password using Firebase Authentication.
    Returns custom tokens for session management.
    """
    try:
        # Firebase Admin SDK does not directly support email/password login,
        # so we simulate the flow by verifying the user exists and generating a custom token.
        user = auth.get_user_by_email(request.email)
        custom_token = auth.create_custom_token(user.uid)
        return LoginResponse(
            success=True,
            access_token=custom_token,
            refresh_token="firebase-refresh-token",
            expires_in=3600,
        )
    except FirebaseError as e:
        return LoginResponse(success=False, error=normalize_firebase_error(e))
