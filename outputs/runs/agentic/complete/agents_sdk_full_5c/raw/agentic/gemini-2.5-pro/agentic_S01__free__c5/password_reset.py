from identity_client import get_auth_client
from identity_models import PasswordResetRequest

def send_password_reset_email(reset_request: PasswordResetRequest) -> bool:
    """
    Sends a password reset email to a user via Firebase Authentication.
    """
    auth = get_auth_client()
    try:
        auth.send_password_reset_email(reset_request.email)
        return True
    except Exception as e:
        print(f"Error sending password reset email: {e}")
        return False
