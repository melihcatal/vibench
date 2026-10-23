from firebase_admin import auth
from identity_client import get_firebase_app
from identity_models import PasswordResetRequest


def send_password_reset_email(reset_request: PasswordResetRequest) -> str:
    get_firebase_app()
    try:
        # This link would typically be sent to the user via a custom email system.
        link = auth.generate_password_reset_link(reset_request.email)
        return link
    except Exception as e:
        raise e
