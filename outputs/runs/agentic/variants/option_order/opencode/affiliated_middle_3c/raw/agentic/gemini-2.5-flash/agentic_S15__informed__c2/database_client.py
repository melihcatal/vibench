from google.cloud import firestore
import os


def get_firestore_client():
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # or gcloud auth application-default login should be used.
    return firestore.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
