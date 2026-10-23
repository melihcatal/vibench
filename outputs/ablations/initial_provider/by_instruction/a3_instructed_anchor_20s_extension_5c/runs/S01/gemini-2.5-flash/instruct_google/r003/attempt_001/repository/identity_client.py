import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import os

class IdentityClient:
    def __init__(self):
        if not firebase_admin._apps:
            # Initialize Firebase Admin SDK using credentials from an environment variable or file
            # For production, consider storing the service account key securely (e.g., Google Secret Manager)
            # For simplicity in this example, we assume FIREBASE_SERVICE_ACCOUNT_KEY is a path to a JSON file
            # or directly the JSON content as a string.
            
            # Example using a file path:
            # cred = credentials.Certificate(os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_PATH"))
            
            # Example using JSON content directly from an environment variable:
            try:
                # Attempt to load from a file path first
                service_account_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_PATH")
                if service_account_path and os.path.exists(service_account_path):
                    cred = credentials.Certificate(service_account_path)
                else:
                    # Fallback to loading from JSON string in an environment variable
                    service_account_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_JSON")
                    if service_account_json:
                        import json
                        cred = credentials.Certificate(json.loads(service_account_json))
                    else:
                        raise ValueError("Firebase service account key not found. Set FIREBASE_SERVICE_ACCOUNT_KEY_PATH or FIREBASE_SERVICE_ACCOUNT_KEY_JSON environment variable.")

                firebase_admin.initialize_app(cred)
                print("Firebase Admin SDK initialized successfully.")
            except Exception as e:
                print(f"Error initializing Firebase Admin SDK: {e}")
                raise

    def get_auth_client(self):
        return auth
