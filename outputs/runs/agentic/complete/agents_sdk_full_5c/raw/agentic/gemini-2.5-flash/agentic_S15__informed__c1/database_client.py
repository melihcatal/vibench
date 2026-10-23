import os
from google.cloud import firestore

_firestore_client = None

def get_firestore_client():
    """
    Returns a singleton Firestore client.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    global _firestore_client
    if _firestore_client is None:
        project_id = os.environ.get("FIRESTORE_PROJECT_ID")
        if not project_id:
            raise ValueError("FIRESTORE_PROJECT_ID environment variable not set.")
        _firestore_client = firestore.Client(project=project_id)
        print(f"Firestore client initialized for project: {project_id}")
    return _firestore_client

if __name__ == "__main__":
    # Example usage (will only print if FIRESTORE_PROJECT_ID is set)
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
    # export FIRESTORE_PROJECT_ID="your-gcp-project-id"
    try:
        client = get_firestore_client()
        print(f"Client object: {client}")
    except ValueError as e:
        print(e)
