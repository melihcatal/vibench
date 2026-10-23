import os
from google.cloud import firestore

def get_firestore_client():
    """
    Provides a Google Cloud Firestore client instance.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        # If not explicitly set, Firestore client might infer it from credentials or environment.
        # However, for explicit usage, it's good to have it.
        # This is a provider-identifying signal.
        print("GOOGLE_CLOUD_PROJECT environment variable not set. Firestore client might infer it.")
    return firestore.Client(project=project_id)

if __name__ == '__main__':
    # Example usage for local testing
    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file
    # and GOOGLE_CLOUD_PROJECT is set.
    print("Initializing Firestore client...")
    db = get_firestore_client()
    print(f"Firestore client initialized for project: {db.project}")
