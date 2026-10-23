from firebase_admin import auth
from identity_client import initialize_firebase_admin
from identity_models import PasswordResetRequest, PasswordResetResponse

initialize_firebase_admin()

def send_password_reset_email(reset_request: PasswordResetRequest) -> PasswordResetResponse:
    """
    Generates a password reset link for the given email.
    """
    try:
        link = auth.generate_password_reset_link(email=reset_request.email)
        return PasswordResetResponse(reset_link=link)
    except auth.UserNotFoundError:
        raise ValueError(f"User with email not found: {reset_request.email}")
    except Exception as e:
        raise RuntimeError(f"Failed to generate password reset link: {e}") from e
