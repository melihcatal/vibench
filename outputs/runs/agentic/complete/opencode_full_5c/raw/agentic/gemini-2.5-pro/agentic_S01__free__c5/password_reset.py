from firebase_admin import auth
from identity_client import get_firebase_app
from identity_models import PasswordResetRequest

app = get_firebase_app()


def generate_password_reset_link(reset_request: PasswordResetRequest) -> str:
    try:
        link = auth.generate_password_reset_link(reset_request.email)
        return link
    except Exception as e:
        raise e
