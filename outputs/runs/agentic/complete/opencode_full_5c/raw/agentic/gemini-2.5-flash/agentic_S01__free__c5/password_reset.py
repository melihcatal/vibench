from identity_client import get_firebase_auth
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    auth = get_firebase_auth()
    try:
        # Firebase generates a password reset link and sends it to the user's email.
        auth.generate_password_reset_link(request.email)
        return PasswordResetResponse(
            message=f"Password reset link sent to {request.email}"
        )
    except Exception as e:
        raise ValueError(f"Failed to initiate password reset: {e}")
