from firebase_admin import auth
from identity_client import get_firebase_app
from identity_models import PasswordResetRequest

def send_password_reset_email(reset_request: PasswordResetRequest) -> str:
    """
    Generates and sends a password reset link to the user's email.
    Firebase Admin SDK handles the email sending.
    """
    get_firebase_app() # Ensure app is initialized

    try:
        # This method generates the link and triggers Firebase to send the email
        # using the default template.
        link = auth.generate_password_reset_link(email=reset_request.email)
        # The link itself is returned, though typically you just need to know
        # the call succeeded.
        return f"Password reset email sent to {reset_request.email}."
    except auth.UserNotFoundError:
        return f"User with email {reset_request.email} not found."
    except Exception as e:
        raise e
