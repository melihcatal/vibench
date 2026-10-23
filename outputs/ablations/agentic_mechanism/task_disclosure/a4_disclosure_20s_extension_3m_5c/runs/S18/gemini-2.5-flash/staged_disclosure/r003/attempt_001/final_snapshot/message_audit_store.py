import os
from google.cloud import firestore

class MessageAuditStore:
    def __init__(self):
        # Google Cloud Firestore client
        # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
        # authenticated via `gcloud auth application-default login`
        self.db = firestore.Client()
        self.collection_ref = self.db.collection('message_audit_records')

    def persist_message(self, message_id: str, message_data: dict):
        """
        Persists a processed message record to Firestore.
        """
        try:
            self.collection_ref.document(message_id).set(message_data)
            print(f"Message {message_id} persisted successfully.")
        except Exception as e:
            print(f"Error persisting message {message_id}: {e}")

    def get_message(self, message_id: str):
        """
        Retrieves a processed message record from Firestore.
        """
        try:
            doc = self.collection_ref.document(message_id).get()
            if doc.exists:
                print(f"Message {message_id} retrieved successfully.")
                return doc.to_dict()
            else:
                print(f"Message {message_id} not found.")
                return None
        except Exception as e:
            print(f"Error retrieving message {message_id}: {e}")
            return None
