import firebase_admin
from firebase_admin import credentials, auth
import os

def register_user(email, password):
    if not firebase_admin._apps:
        # Initialize Firebase Admin SDK if not already initialized
        # This assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
        # or a service account key file is provided.
        # For this example, we'll assume a service account key file path
        # is available or the environment is configured for Firebase.
        try:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
        except Exception as e:
            # Fallback for local development if ApplicationDefault fails
            # Replace with your actual service account key path in a real application
            service_account_key_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH", "path/to/your/serviceAccountKey.json")
            if os.path.exists(service_account_key_path):
                cred = credentials.Certificate(service_account_key_path)
                firebase_admin.initialize_app(cred)
            else:
                raise Exception(f"Firebase initialization failed: {e}. Please ensure GOOGLE_APPLICATION_CREDENTIALS is set or a valid service account key file is provided at {service_account_key_path}")


    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return {"uid": user.uid, "email": user.email}
    except Exception as e:
        raise Exception(f"Failed to create user: {e}")
