from firebase_admin import auth
from identity_client import initialize_firebase

initialize_firebase()


def send_password_reset_email(email: str) -> str:
    """
    Generates a password reset link for the given email.

    In a real application, this link would be sent to the user's email address.
    """
    try:
        link = auth.generate_password_reset_link(email)
        return link
    except auth.UserNotFoundError:
        # Handle case where user does not exist
        raise ValueError("User with the provided email does not exist.")
    except Exception as e:
        # Handle other potential errors
        raise e
