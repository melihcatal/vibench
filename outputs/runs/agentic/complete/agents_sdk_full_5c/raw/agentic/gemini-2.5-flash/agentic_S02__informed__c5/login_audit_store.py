import os
import datetime
from google.cloud import firestore

class FirestoreAuditStore:
    def __init__(self, project_id: str, collection_name: str = "federated_login_audits"):
        self.db = firestore.Client(project=project_id)
        self.collection_ref = self.db.collection(collection_name)

    def add_audit_record(self, event_type: str, user_id: str, details: dict) -> str:
        """Adds a federated-login audit record to Firestore."""
        record = {
            "event_type": event_type,
            "user_id": user_id,
            "timestamp": datetime.datetime.now(tz=datetime.timezone.utc),
            "details": details
        }
        try:
            doc_ref = self.collection_ref.add(record)
            return f"Audit record added with ID: {doc_ref[1].id}"
        except Exception as e:
            return f"Error adding audit record to Firestore: {e}"

    def get_audit_records(self, user_id: str = None, limit: int = 10) -> list[dict]:
        """Retrieves audit records, optionally filtered by user_id."""
        query = self.collection_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(limit)
        if user_id:
            query = query.where("user_id", "==", user_id)
        
        results = []
        for doc in query.stream():
            record = doc.to_dict()
            record["id"] = doc.id
            results.append(record)
        return results

if __name__ == "__main__":
    # Google Cloud project ID is usually picked up from the environment or gcloud config
    # For explicit setting, uncomment and replace 'your-gcp-project-id'
    # GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication

    # For demonstration, we'll assume a project ID is available or credentials are set up.
    # If running locally, make sure `gcloud auth application-default login` has been run
    # or GOOGLE_APPLICATION_CREDENTIALS points to a service account key file.
    
    # Replace with your actual project ID
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id") 

    if project_id == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable or configure application default credentials.")
    else:
        audit_store = FirestoreAuditStore(project_id=project_id)

        print("--- Storing Audit Records ---")
        # Example audit records
        record_id_1 = audit_store.add_audit_record(
            event_type="login_success",
            user_id="alice@example.com",
            details={
                "provider": "Auth0",
                "ip_address": "192.168.1.100",
                "device": "desktop browser"
            }
        )
        print(record_id_1)

        record_id_2 = audit_store.add_audit_record(
            event_type="token_exchange_failed",
            user_id="bob@example.com",
            details={
                "provider": "Auth0",
                "error": "invalid_grant",
                "ip_address": "203.0.113.45"
            }
        )
        print(record_id_2)
        
        print("\n--- Retrieving Audit Records for Alice---")
        alice_audits = audit_store.get_audit_records(user_id="alice@example.com")
        for audit in alice_audits:
            print(audit)

        print("\n--- Retrieving Latest 5 Audit Records (All Users)---")
        recent_audits = audit_store.get_audit_records(limit=5)
        for audit in recent_audits:
            print(audit)
