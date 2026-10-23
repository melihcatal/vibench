import os
from google.cloud import firestore

def get_firestore_client():
    """
    Initializes and returns a Google Firestore client.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment.
    """
    return firestore.Client()

if __name__ == "__main__":
    # Example usage (for local testing, not part of the final integration)
    try:
        client = get_firestore_client()
        print("Firestore client initialized successfully.")
    except Exception as e:
        print(f"Error initializing Firestore client: {e}")
