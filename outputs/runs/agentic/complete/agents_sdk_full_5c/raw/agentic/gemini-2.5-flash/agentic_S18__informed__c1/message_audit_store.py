import os
from datetime import datetime, timezone
from google.cloud import firestore

def persist_message_record(collection_name: str, record: dict) -> str:
    """Persists a processed message record to Google Firestore."""
    # Firestore client automatically uses GOOGLE_APPLICATION_CREDENTIALS
    db = firestore.Client() 

    # Add a timestamp if not already present
    if "processed_at" not in record:
        record["processed_at"] = datetime.now(timezone.utc).isoformat()

    try:
        # If a document ID is provided in the record, use it, otherwise Firestore will auto-generate one
        if "id" in record:
            doc_ref = db.collection(collection_name).document(record["id"])
            doc_ref.set(record)
            return f"Record with ID {record['id']} persisted to Firestore collection {collection_name}."
        else:
            doc_ref = db.collection(collection_name).add(record)
            return f"Record with auto-generated ID {doc_ref[1].id} persisted to Firestore collection {collection_name}."
    except Exception as e:
        return f"Error persisting record to Firestore: {e}"

if __name__ == '__main__':
    # The project ID is usually inferred from GOOGLE_APPLICATION_CREDENTIALS
    # or explicitly passed during Client initialization. We'll rely on env here.
    # No explicit project_id needed for client init if GOOGLE_APPLICATION_CREDENTIALS is set.

    audit_collection_name = os.environ.get("FIRESTORE_AUDIT_COLLECTION", "message_audit_log")

    sample_record_1 = {
        "original_message_id": "msg-abc-123",
        "event_type": "user_login",
        "status": "SUCCESS",
        "user_id": "U456",
        "summary": "User U456 successfully logged in."
    }
    result_1 = persist_message_record(audit_collection_name, sample_record_1)
    print(result_1)

    sample_record_2 = {
        "id": "custom-audit-id-789", # Example of providing a custom document ID
        "original_message_id": "msg-xyz-789",
        "event_type": "payment_failed",
        "status": "FAILED",
        "error_code": "ERR-PAY-001",
        "details": "Credit card declined."
    }
    result_2 = persist_message_record(audit_collection_name, sample_record_2)
    print(result_2)
