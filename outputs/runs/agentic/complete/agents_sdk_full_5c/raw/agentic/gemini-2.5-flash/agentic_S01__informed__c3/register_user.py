import firebase_admin
from firebase_admin import credentials, auth
import os

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    try:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)
    except Exception:
        # Fallback for local testing if GOOGLE_APPLICATION_CREDENTIALS is not set
        # This assumes a service account key file is available at a known path
        # In a real application, use GOOGLE_APPLICATION_CREDENTIALS or similar
        print("GOOGLE_APPLICATION_CREDENTIALS not found, attempting to load from local file.")
        service_account_key_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_PATH", "path/to/your/serviceAccountKey.json")
        if os.path.exists(service_account_key_path):
            cred = credentials.Certificate(service_account_key_path)
            firebase_admin.initialize_app(cred)
        else:
            raise FileNotFoundError(f"Firebase service account key not found at {service_account_key_path}")

def register_user(email: str, password: str, display_name: str = None):
    """
    Creates a new user account with email and password using Firebase Authentication.
    """
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        return {"uid": user.uid, "email": user.email, "message": "User registered successfully"}
    except Exception as e:
        return {"error": str(e)}

