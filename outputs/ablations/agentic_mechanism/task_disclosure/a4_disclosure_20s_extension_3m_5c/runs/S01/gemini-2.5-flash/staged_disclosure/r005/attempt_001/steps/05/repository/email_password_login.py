import firebase_admin
from firebase_admin import credentials, auth
import os

# IMPORTANT: For production, it's highly recommended to use environment variables for sensitive information.
# For example, set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your Firebase service account key file.
# Alternatively, you can explicitly pass credentials using `credentials.Certificate('path/to/your/serviceAccountKey.json')`
# if the environment variable is not set.

_firebase_app = None

def _get_firebase_app():
    """Initializes and returns the Firebase app instance, ensuring it's only initialized once."""
    global _firebase_app
    if _firebase_app is None:
        try:
            # Attempt to initialize with default credentials (e.g., GOOGLE_APPLICATION_CREDENTIALS env var)
            _firebase_app = firebase_admin.initialize_app()
        except ValueError:
            # If default initialization fails (e.g., no env var), try explicit path from a placeholder env var
            service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY_PATH')
            if service_account_path and os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
                _firebase_app = firebase_admin.initialize_app(cred)
            else:
                raise RuntimeError("Firebase Admin SDK credentials not found. Please set GOOGLE_APPLICATION_CREDENTIALS "
                                   "or FIREBASE_SERVICE_ACCOUNT_KEY_PATH environment variable to a valid service account key file path.")
    return _firebase_app

def sign_in_or_create_user_and_get_custom_token(email: str, password: str) -> str:
    """
    Attempts to retrieve a user by email. If the user doesn't exist, it creates one with the given password.
    Finally, it generates and returns a custom Firebase ID token for the user.
    This custom token can be used by a client-side Firebase SDK to sign in.

    Args:
        email: The user's email address.
        password: The user's password.

    Returns:
        A string representation of the custom Firebase ID token.
    """
    app = _get_firebase_app()
    try:
        user = auth.get_user_by_email(email, app=app)
    except auth.UserNotFoundError:
        # User not found, create a new one.
        user = auth.create_user(email=email, password=password, app=app)

    # Generate a custom token for the user.
    custom_token = auth.create_custom_token(user.uid, app=app)
    return custom_token.decode('utf-8')
