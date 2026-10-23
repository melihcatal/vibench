from identity_client import firebase_auth
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    """
    Initiates a password reset flow by generating a password reset link.
    """
    try:
        reset_link = firebase_auth.generate_password_reset_link(request.email)
        return PasswordResetResponse(reset_link=reset_link)
    except Exception as e:
        raise RuntimeError(f"Failed to generate password reset link: {e}")
