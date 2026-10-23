import os
import firebase_admin
from firebase_admin import credentials

_firebase_app = None

def get_firebase_app():
    global _firebase_app
    if _firebase_app is None:
        # Load Firebase service account key from environment variable or file.
        # It's recommended to set GOOGLE_APPLICATION_CREDENTIALS for production.
        # For this example, we'll try to load from a file specified by an env var.
        service_account_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_PATH")

        if service_account_path and os.path.exists(service_account_path):
            cred = credentials.Certificate(service_account_path)
        else:
            # Fallback for local development if GOOGLE_APPLICATION_CREDENTIALS is set
            # and contains the JSON content directly, or if using a default ADC.
            # In a production GKE/Cloud Run environment, ADC will handle authentication automatically.
            print("Warning: FIREBASE_SERVICE_ACCOUNT_KEY_PATH not found or not set. "
                  "Relying on GOOGLE_APPLICATION_CREDENTIALS or default ADC.")
            cred = credentials.ApplicationDefault()

        _firebase_app = firebase_admin.initialize_app(cred)
    return _firebase_app

if __name__ == '__main__':
    # This block is for demonstration/testing only
    # Set FIREBASE_SERVICE_ACCOUNT_KEY_PATH to your Firebase service account JSON file
    # os.environ["FIREBASE_SERVICE_ACCOUNT_KEY_PATH"] = "./path/to/your/serviceAccountKey.json"
    # try:
    #     app = get_firebase_app()
    #     print(f"Firebase app initialized successfully: {app.name}")
    # except Exception as e:
    #     print(f"Error initializing Firebase app: {e}")
    pass
