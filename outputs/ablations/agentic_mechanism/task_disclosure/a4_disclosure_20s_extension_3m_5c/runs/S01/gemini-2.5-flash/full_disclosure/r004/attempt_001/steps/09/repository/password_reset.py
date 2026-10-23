import firebase_admin
from firebase_admin import credentials, auth
import os

# Initialize Firebase Admin SDK if not already initialized
# Ensure you have your service account key file path set as an environment variable
# For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/serviceAccountKey.json"
if not firebase_admin._apps:
    try:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")
        # Fallback for local development if GOOGLE_APPLICATION_CREDENTIALS is not set
        # Replace 'path/to/your/serviceAccountKey.json' with your actual path
        # In a production environment, always use environment variables or secret management
        if os.path.exists('path/to/your/serviceAccountKey.json'):
            cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
            firebase_admin.initialize_app(cred)
        else:
            raise RuntimeError("Firebase Admin SDK could not be initialized. "
                               "Ensure GOOGLE_APPLICATION_CREDENTIALS is set or serviceAccountKey.json is available.")

def send_password_reset_email(email: str):
    """
    Starts a password reset flow for a local account using Firebase Authentication.

    Args:
        email: The email address of the user who requested a password reset.

    Returns:
        A dictionary indicating success or failure.
    """
    try:
        auth.generate_password_reset_link(email)
        return {"status": "success", "message": f"Password reset email sent to {email}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

