import os
from firebase_admin import auth
from identity_client import get_firebase_app
from identity_models import PasswordResetRequest, PasswordResetResponse

def password_reset(email: str) -> PasswordResetResponse:
    app = get_firebase_app()
    try:
        link = auth.generate_password_reset_link(email, app=app)
        return PasswordResetResponse(
            reset_link=link,
            email=email
        )
    except Exception as e:
        raise ValueError(f"Password reset failed: {str(e)}")