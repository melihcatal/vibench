
from google.cloud import firestore
import os

def get_firestore_client():
    """
    Returns a Google Cloud Firestore client.

    The client is initialized using credentials from the GOOGLE_APPLICATION_CREDENTIALS
    environment variable or other default mechanisms provided by the Google Cloud
    client library.
    """
    # Initialize Firestore DB client
    # The project ID is usually inferred from the environment (e.g., GOOGLE_CLOUD_PROJECT
    # environment variable, gcloud CLI configuration, or metadata server on GCP).
    # You can explicitly set it if needed: firestore.Client(project='your-project-id')
    return firestore.Client()

