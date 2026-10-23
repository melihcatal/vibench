import os
from google.cloud import firestore

class FirestoreClient:
    """Provides a singleton Firestore client instance and configuration."""

    _client = None

    @classmethod
    def get_client(cls):
        """Returns a configured Firestore client."""
        if cls._client is None:
            # Assumes GOOGLE_APPLICATION_CREDENTIALS env var is set
            cls._client = firestore.Client()
        return cls._client

    @staticmethod
    def get_collection_ref(collection_name: str):
        """Returns a reference to a Firestore collection."""
        return FirestoreClient.get_client().collection(collection_name)

if __name__ == '__main__':
    # Example usage:
    # client = FirestoreClient.get_client()
    # print(f"Firestore client initialized: {client}")
    # collection_ref = FirestoreClient.get_collection_ref("my_test_collection")
    # print(f"Collection reference: {collection_ref.id}")
    pass
