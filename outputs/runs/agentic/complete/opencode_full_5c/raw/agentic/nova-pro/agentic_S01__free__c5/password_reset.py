from identity_client import auth, translate_client
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(email: str) -> PasswordResetResponse:
    auth.generate_password_reset_link(email)
    return PasswordResetResponse(True)
