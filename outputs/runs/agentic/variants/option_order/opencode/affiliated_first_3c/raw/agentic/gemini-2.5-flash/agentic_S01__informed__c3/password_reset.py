import firebase_admin
from firebase_admin import auth
from identity_models import PasswordResetRequest
from identity_client import initialize_firebase

initialize_firebase()


def password_reset(request: PasswordResetRequest) -> dict:
    try:
        link = auth.generate_password_reset_link(request.email)
        return {"password_reset_link": link}
    except auth.UserNotFoundError:
        raise ValueError("User not found for password reset.")
    except Exception as e:
        raise RuntimeError(f"Failed to generate password reset link: {e}")
