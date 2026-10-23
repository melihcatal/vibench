import os

from google.cloud import firestore
from google.oauth2 import service_account


def get_firestore_client():
    """Initialize and return a Firestore client using service account credentials."""
    creds = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    return firestore.Client(credentials=creds)
