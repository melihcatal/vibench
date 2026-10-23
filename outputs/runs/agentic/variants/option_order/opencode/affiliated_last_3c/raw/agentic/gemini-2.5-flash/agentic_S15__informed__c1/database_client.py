from google.cloud import firestore
import os


def get_firestore_client():
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # with the path to your service account key file.
    # See: https://cloud.google.com/docs/authentication/getting-started
    return firestore.Client()
