import os
import datetime
from google.cloud import firestore
from identity_models import AuditRecord

# Configure Google Cloud Firestore client
# GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
db = firestore.Client()
AUDIT_COLLECTION = "federated_login_audit"

def persist_audit_record(record: AuditRecord) -> dict:
    """
    Persists a federated-login audit record in Google Firestore.
    """
    try:
        doc_ref = db.collection(AUDIT_COLLECTION).document(record.event_id)
        doc_ref.set(record.to_dict())
        return {"status": "success", "event_id": record.event_id}
    except Exception as e:
        return {"status": "error", "message": f"Failed to persist audit record: {e}"}

def get_audit_record(event_id: str) -> Optional[AuditRecord]:
    """
    Retrieves an audit record by its event ID from Google Firestore.
    """
    try:
        doc_ref = db.collection(AUDIT_COLLECTION).document(event_id)
        doc = doc_ref.get()
        if doc.exists:
            return AuditRecord.from_dict(doc.to_dict())
        return None
    except Exception as e:
        print(f"Error retrieving audit record: {e}")
        return None

if __name__ == "__main__":
    # Example Usage:
    new_audit_record = AuditRecord(
        event_id=f"test_event_{datetime.datetime.now().isoformat().replace('.', '')}",
        timestamp=datetime.datetime.now().isoformat() + "Z",
        user_id="user_abc",
        event_type="LOGIN_SUCCESS",
        ip_address="10.0.0.1",
        user_agent="Mozilla/5.0",
        status="SUCCESS",
        details={"idp": "Auth0", "session_duration": 3600}
    )

    print("Persisting audit record...")
    result = persist_audit_record(new_audit_record)
    print(result)

    if result.get("status") == "success":
        print(f"\nRetrieving audit record for event ID: {new_audit_record.event_id}")
        retrieved_record = get_audit_record(new_audit_record.event_id)
        if retrieved_record:
            print("Retrieved successfully:")
            print(retrieved_record.to_dict())
        else:
            print("Record not found.")
