import os
import firebase_admin
from firebase_admin import credentials


def initialize_firebase():
    if not firebase_admin._apps:
        # Check if GOOGLE_APPLICATION_CREDENTIALS is set
        if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
            cred = credentials.ApplicationDefault()
        else:
            # Fallback for environments where GOOGLE_APPLICATION_CREDENTIALS is not set,
            # but a service account key JSON is directly available or for local testing.
            # In a real-world scenario, GOOGLE_APPLICATION_CREDENTIALS is preferred.
            # This part might need adjustment based on specific deployment.
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable not set."
            )
        firebase_admin.initialize_app(cred)


initialize_firebase()
