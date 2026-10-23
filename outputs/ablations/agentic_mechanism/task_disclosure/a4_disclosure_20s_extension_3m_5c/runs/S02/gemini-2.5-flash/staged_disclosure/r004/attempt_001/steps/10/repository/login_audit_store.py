import os
from datetime import datetime
from google.cloud import firestore

class LoginAuditStore:
    def __init__(self):
        # Initialize Firestore client
        # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
        # or that the application is running in a Google Cloud environment
        self.db = firestore.Client()
        self.collection_name = "federated_login_audits"

    def record_audit_event(self, user_id: str, provider: str, timestamp: datetime = None):
        """
        Records a federated login audit event in Firestore.
        """
        if timestamp is None:
            timestamp = datetime.utcnow()

        audit_record = {
            "user_id": user_id,
            "provider": provider,
            "timestamp": timestamp,
            "event_type": "federated_login"
        }

        try:
            doc_ref = self.db.collection(self.collection_name).add(audit_record)
            print(f"Audit record added with ID: {doc_ref[1].id}")
            return doc_ref[1].id
        except Exception as e:
            print(f"Error recording audit event: {e}")
            raise

if __name__ == "__main__":
    # Example Usage:
    # To run this example, make sure you have authenticated to Google Cloud
    # and have a Firestore database set up in your project.
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable if running locally.

    # audit_store = LoginAuditStore()
    # try:
    #     audit_store.record_audit_event(user_id="user123", provider="google")
    #     audit_store.record_audit_event(user_id="user456", provider="azure_ad")
    # except Exception as e:
    #     print(f"Failed to record audit events: {e}")
    print("LoginAuditStore class created. Example usage is commented out.")
