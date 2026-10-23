from google.cloud import firestore
import os

def get_firestore_client():
    # Initialize Google Cloud Firestore client
    # Environment variable GOOGLE_APPLICATION_CREDENTIALS should be set
    # or the project ID should be explicitly passed if not running in GCP
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if project_id:
        return firestore.Client(project=project_id)
    else:
        return firestore.Client()
