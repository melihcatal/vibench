import firebase_admin
from firebase_admin import credentials, auth
import os

# Initialize Firebase Admin SDK
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# to the path of your service account key file.
if not firebase_admin._apps:
    try:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)
    except Exception as e:
        # Fallback for local development if GOOGLE_APPLICATION_CREDENTIALS isn't set
        # This part assumes a service-account.json in the current directory for dev
        # For production, GOOGLE_APPLICATION_CREDENTIALS env var is preferred
        service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if service_account_path and os.path.exists(service_account_path):
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
        else:
            print(f"Firebase initialization failed: {e}")
            print(
                "Please set GOOGLE_APPLICATION_CREDENTIALS environment variable to your service account key file."
            )
            # As a last resort, attempt to initialize without specific credentials,
            # which might work in some GCP environments with default service accounts.
            try:
                firebase_admin.initialize_app()
            except Exception as inner_e:
                print(
                    f"Firebase initialization without explicit credentials also failed: {inner_e}"
                )
                raise RuntimeError("Failed to initialize Firebase Admin SDK.")

# Expose the auth client
firebase_auth = auth
