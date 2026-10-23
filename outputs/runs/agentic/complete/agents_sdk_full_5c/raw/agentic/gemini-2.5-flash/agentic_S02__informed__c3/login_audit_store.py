from google.cloud import firestore
from datetime import datetime
from identity_client import IdentityClientConfig

def store_audit_record(event_data: dict) -> str:
    if not IdentityClientConfig.GCP_PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID must be set for Firestore integration.")

    # Instantiates a client. This also requires GOOGLE_APPLICATION_CREDENTIALS to be set
    # or running in a GCP environment with appropriate permissions.
    db = firestore.Client(project=IdentityClientConfig.GCP_PROJECT_ID)

    collection_ref = db.collection("login_audit_records")
    
    # Add a timestamp if not already present in event_data
    if "timestamp" not in event_data:
        event_data["timestamp"] = datetime.utcnow()

    doc_ref = collection_ref.add(event_data)
    return doc_ref[1].id

if __name__ == "__main__":
    example_audit_event = {
        "user_id": "auth0|12345",
        "event_type": "LOGIN_SUCCESS",
        "ip_address": "192.168.1.100",
        "provider": "Auth0",
        "details": "User successfully logged in via OAuth callback."
    }
    if IdentityClientConfig.GCP_PROJECT_ID:
        print("--- Persisting Audit Record using Google Firestore ---")
        try:
            document_id = store_audit_record(example_audit_event)
            print(f"Audit record stored with document ID: {document_id}")
        except Exception as e:
            print(f"Error storing audit record: {e}")
            print("Ensure GOOGLE_APPLICATION_CREDENTIALS and GCP_PROJECT_ID are correctly configured.")
    else:
        print("GCP_PROJECT_ID not set. Cannot run Google Firestore example.")
