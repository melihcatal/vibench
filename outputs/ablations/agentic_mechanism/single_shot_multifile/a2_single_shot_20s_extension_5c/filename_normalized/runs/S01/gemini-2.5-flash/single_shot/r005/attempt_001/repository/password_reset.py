from identity_client import config
from identity_models import PasswordResetRequest

def password_reset(request: PasswordResetRequest) -> str:
    """
    Starts a password reset flow for a Firebase user account by generating a password reset link.
    Returns the password reset link.
    """
    try:
        link = config.auth_client.generate_password_reset_link(request.email)
        return link
    except Exception as e:
        raise RuntimeError(f"Failed to generate password reset link for {request.email}: {e}")
