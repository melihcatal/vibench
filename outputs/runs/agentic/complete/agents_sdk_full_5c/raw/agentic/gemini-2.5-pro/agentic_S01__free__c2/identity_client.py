import os
import firebase_admin
from firebase_admin import credentials

_app = None

def get_firebase_app():
    """Initializes and returns the Firebase app instance."""
    global _app
    if _app:
        return _app

    # The GOOGLE_APPLICATION_CREDENTIALS env var is the standard way
    # the SDK finds the service account key file.
    if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
        # For local development, you might place the service account key
        # at a known path.
        # This check is illustrative; in a real app, configuration
        # would be more robust.
        cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH", "serviceAccountKey.json")
        if not os.path.exists(cred_path):
            raise FileNotFoundError(
                "Firebase credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS "
                "or FIREBASE_SERVICE_ACCOUNT_KEY_PATH."
            )
        cred = credentials.Certificate(cred_path)
    else:
        # Use Application Default Credentials
        cred = credentials.ApplicationDefault()

    _app = firebase_admin.initialize_app(cred)
    return _app

def get_firebase_api_key():
    """Retrieves the Firebase Web API Key from environment variables."""
    api_key = os.getenv("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")
    return api_key

# Initialize on import
get_firebase_app()
