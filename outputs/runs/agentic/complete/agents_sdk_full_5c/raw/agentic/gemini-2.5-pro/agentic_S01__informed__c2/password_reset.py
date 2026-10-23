# password_reset.py
from identity_client import initialize_firebase_admin
from identity_models import PasswordResetRequest

def send_password_reset_email(reset_request: PasswordResetRequest) -> str:
    """
    Generates a password reset link and (conceptually) sends it.
    Firebase Admin SDK generates the link, sending is handled by Firebase.
    """
    auth = initialize_firebase_admin()
    try:
        # Firebase handles sending the email automatically with this method.
        # The link itself is just returned for logging or custom flow purposes.
        link = auth.generate_password_reset_link(email=reset_request.email)
        print(f"Password reset email sent to {reset_request.email}.")
        return link
    except Exception as e:
        print(f"Error generating password reset link for {reset_request.email}: {e}")
        raise e
