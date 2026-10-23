from firebase_admin import auth
from identity_models import PasswordResetRequest
from identity_client import initialize_firebase_app


def initiate_password_reset(request_data: PasswordResetRequest) -> str:
    """
    Generates a password reset link for the given email.
    """
    initialize_firebase_app()
    try:
        link = auth.generate_password_reset_link(request_data.email)
        return link
    except Exception as e:
        # Handle errors e.g. user not found
        raise e
