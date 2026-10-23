from identity_client import get_firebase_auth_client
from identity_models import PasswordResetRequest


def password_reset(request: PasswordResetRequest):
    auth_client = get_firebase_auth_client()
    try:
        auth_client.generate_password_reset_link(request.email)
        return {"message": f"Password reset email sent to {request.email}"}
    except Exception as e:
        raise RuntimeError(f"Failed to send password reset email: {e}")
