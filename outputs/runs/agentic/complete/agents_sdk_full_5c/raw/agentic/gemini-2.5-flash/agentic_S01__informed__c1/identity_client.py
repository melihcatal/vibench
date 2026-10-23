import os
import firebase_admin
from firebase_admin import credentials

_firebase_app = None

def get_firebase_app():
    """
    Initializes and returns the Firebase Admin SDK app instance.
    The path to the service account key JSON file should be provided via
    the FIREBASE_CREDENTIALS_PATH environment variable.
    """
    global _firebase_app
    if _firebase_app is None:
        credentials_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
        if not credentials_path:
            raise EnvironmentError("FIREBASE_CREDENTIALS_PATH environment variable not set.")
        
        # Check if the path is absolute or relative to the current working directory
        if not os.path.isabs(credentials_path):
            credentials_path = os.path.join(os.getcwd(), credentials_path)

        if not os.path.exists(credentials_path):
            raise FileNotFoundError(f"Firebase credentials file not found at: {credentials_path}")

        cred = credentials.Certificate(credentials_path)
        _firebase_app = firebase_admin.initialize_app(cred)
    return _firebase_app

if __name__ == '__main__':
    # Example usage:
    # Set the environment variable before running:
    # export FIREBASE_CREDENTIALS_PATH="./path/to/your/serviceAccountKey.json"
    # Or, for local testing, create a dummy file and set the env var
    # try:
    #     app = get_firebase_app()
    #     print("Firebase Admin SDK initialized successfully.")
    # except Exception as e:
    #     print(f"Error initializing Firebase Admin SDK: {e}")
    pass
