import firebase_admin
from firebase_admin import auth
from identity_client import get_firebase_app
from identity_models import PasswordResetRequest, PasswordResetResponse


def start_password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    app = get_firebase_app()
    try:
        # Firebase Admin SDK provides a way to generate a password reset link.
        link = auth.generate_password_reset_link(request.email, app=app)
        return PasswordResetResponse(email=request.email, reset_link=link)
    except Exception as e:
        raise Exception(f"Firebase password reset failed: {e}")
