from google.cloud import firestore
import os

class LoginAuditStore:
    def __init__(self):
        # Initialize Firestore client
        # The GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
        # or the service account key file should be placed in a discoverable location.
        self.db = firestore.Client()
        self.collection_name = os.environ.get("FIRESTORE_AUDIT_COLLECTION", "federated_login_audits")

    def persist_audit_record(self, record: dict):
        """
        Persists a federated login audit record to Firestore.
        """
        try:
            doc_ref = self.db.collection(self.collection_name).add(record)
            print(f"Audit record added with ID: {doc_ref[1].id}")
            return doc_ref[1].id
        except Exception as e:
            print(f"Error persisting audit record: {e}")
            raise

