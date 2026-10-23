from identity_client import get_auth_client
from identity_models import PasswordResetRequest


def password_reset(req: PasswordResetRequest) -> str:
    auth = get_auth_client()
    try:
        result = auth.send_password_reset_email(req.email)
        return result
    except Exception as e:
        print(f"An error occurred sending password reset email: {e}")
        raise
