from identity_client import get_auth_client
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    auth = get_auth_client()
    try:
        auth.generate_password_reset_link(request.email)
        return PasswordResetResponse("Password reset email sent successfully.")
    except Exception as e:
        raise ValueError(f"Firebase password reset failed: {e}")
