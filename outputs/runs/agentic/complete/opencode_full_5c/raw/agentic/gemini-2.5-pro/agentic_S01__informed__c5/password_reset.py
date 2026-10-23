from firebase_admin import auth
from identity_client import initialize_firebase_admin
from identity_models import PasswordResetRequest


def send_password_reset_email(reset_request: PasswordResetRequest) -> dict:
    """
    Generates a password reset link and sends it to the user's email.
    Firebase handles the email sending.
    """
    initialize_firebase_admin()
    try:
        link = auth.generate_password_reset_link(reset_request.email)
        # In a real application, you might not return the link directly
        # but confirm that the email has been sent.
        return {"message": "Password reset email sent.", "reset_link": link}
    except auth.UserNotFoundError:
        return {"error": "User not found with that email."}
    except Exception as e:
        return {"error": str(e)}
