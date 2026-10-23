import os
from google.cloud.firestore import Client

_firestore_client = None

def get_firestore_client() -> Client:
    """
    Provides a singleton Google Cloud Firestore client.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    global _firestore_client
    if _firestore_client is None:
        # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
                  "Firestore client might not authenticate correctly.")
        _firestore_client = Client()
    return _firestore_client
