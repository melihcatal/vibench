from identity_client import identity_client
from identity_models import PasswordResetRequest

def request_password_reset(reset_request: PasswordResetRequest) -> str:
    try:
        # Firebase Admin SDK generates a password reset link which can be sent to the user.
        # This function returns the link, which a real application would then email to the user.
        link = identity_client.auth_sdk.generate_password_reset_link(reset_request.email)
        return link
    except Exception as e:
        raise RuntimeError(f"Failed to request password reset: {e}")
