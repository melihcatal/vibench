import os
from google.cloud import firestore

def get_firestore_client():
    """Initializes and returns a Google Cloud Firestore client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # run in a Google Cloud environment (e.g., Cloud Run, GKE) with appropriate permissions.
    # For local development, set GOOGLE_APPLICATION_CREDENTIALS to the path of your service account key file.
    # e.g., os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    # The project ID will be automatically detected when running in a Google Cloud environment
    # or if GOOGLE_CLOUD_PROJECT environment variable is set.
    # Alternatively, you can explicitly pass project=project_id to firestore.Client()
    return firestore.Client()

if __name__ == "__main__":
    # Example usage (for testing client initialization)
    try:
        client = get_firestore_client()
        print(f"Firestore client initialized successfully for project: {client.project}")
    except Exception as e:
        print(f"Error initializing Firestore client: {e}")
