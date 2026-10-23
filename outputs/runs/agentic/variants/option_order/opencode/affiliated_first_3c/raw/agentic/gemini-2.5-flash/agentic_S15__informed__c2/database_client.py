import os
from google.cloud import firestore


class FirestoreClient:
    _db = None

    @classmethod
    def get_client(cls):
        if cls._db is None:
            # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
            # For local development, ensure your gcloud is authenticated
            # gcloud auth application-default login
            cls._db = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
        return cls._db
