from identity_client import initialize_firebase_admin
from identity_models import PasswordResetRequest, PasswordResetResponse

def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    auth = initialize_firebase_admin()
    try:
        # Firebase sends the password reset email directly.
        auth.generate_password_reset_link(request['email'])
        return {"message": f"Password reset email sent to {request['email']}"}
    except Exception as e:
        raise RuntimeError(f"Failed to initiate password reset: {e}")

