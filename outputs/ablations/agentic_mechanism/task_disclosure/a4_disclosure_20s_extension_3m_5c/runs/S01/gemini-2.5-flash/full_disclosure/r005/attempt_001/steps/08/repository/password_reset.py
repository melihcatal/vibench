import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK (replace with your actual credentials)
# Make sure to set GOOGLE_APPLICATION_CREDENTIALS environment variable
# or provide the path to your service account key file.
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def start_password_reset(email: str) -> str:
    """
    Starts a password reset flow for a local account using Firebase Authentication.

    Args:
        email: The email of the user requesting a password reset.

    Returns:
        The password reset link.
    """
    try:
        link = auth.generate_password_reset_link(email)
        return link
    except Exception as e:
        raise Exception(f"Error generating password reset link: {e}")
