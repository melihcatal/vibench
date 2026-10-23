import firebase_admin
from firebase_admin import credentials, auth
import os

def register_user(email, password):
    if not firebase_admin._apps:
        # Initialize Firebase Admin SDK if not already initialized
        # Replace 'path/to/your/serviceAccountKey.json' with the actual path to your Firebase service account key
        # or use an environment variable for security in production.
        # For example: os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_PATH")
        cred = credentials.Certificate(os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_PATH", "path/to/your/serviceAccountKey.json"))
        firebase_admin.initialize_app(cred)

    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return {"uid": user.uid, "email": user.email}
    except Exception as e:
        raise Exception(f"Failed to register user: {e}")

