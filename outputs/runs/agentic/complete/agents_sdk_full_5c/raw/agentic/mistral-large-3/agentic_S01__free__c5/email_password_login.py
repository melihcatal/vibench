import os
from firebase_admin import auth
from identity_client import get_firebase_app
from identity_models import LoginRequest, LoginResponse

def email_password_login(email: str, password: str) -> LoginResponse:
    app = get_firebase_app()
    try:
        user = auth.get_user_by_email(email, app=app)
        custom_token = auth.create_custom_token(user.uid, app=app)
        # Simulate ID token exchange for demonstration
        id_token = auth.sign_in_with_email_and_password(
            email=email, password=password
        ).get("idToken")
        return LoginResponse(
            access_token=id_token,
            refresh_token="simulated_refresh_token",
            user_id=user.uid
        )
    except Exception as e:
        raise ValueError(f"Login failed: {str(e)}")