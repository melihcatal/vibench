import os
import datetime
from google.cloud import firestore

def persist_processed_message(collection_name: str, message_record: dict, document_id: str = None, project_id: str = None) -> str:
    """Persists processed message records for later lookup using Google Cloud Firestore."""
    db = firestore.Client(project=project_id or os.getenv("GOOGLE_CLOUD_PROJECT"))

    # Add a timestamp if not present
    if "processed_at" not in message_record:
        message_record["processed_at"] = datetime.datetime.now(datetime.timezone.utc)

    if document_id:
        doc_ref = db.collection(collection_name).document(document_id)
        doc_ref.set(message_record)
        print(f"Document updated with ID: {document_id}")
    else:
        doc_ref = db.collection(collection_name).add(message_record)
        document_id = doc_ref[1].id # doc_ref is a tuple (timestamp, document_reference)
        print(f"Document added with ID: {document_id}")
    return document_id

if __name__ == "__main__":
    # Example usage (requires GOOGLE_CLOUD_PROJECT env var set)
    # from your shell, run:
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # python message_audit_store.py
    audit_record_1 = {
        "original_message_id": "msg-abc-123",
        "event_type": "user_signup",
        "status": "processed",
        "payload_summary": "New user with email example@example.com signed up.",
        "processed_by_service": "user_onboarding_service"
    }
    audit_record_2 = {
        "original_message_id": "msg-def-456",
        "event_type": "product_update",
        "status": "failed",
        "error_reason": "invalid_product_id",
        "processed_by_service": "catalog_sync_service"
    }

    doc_id_1 = persist_processed_message("message_audit_logs", audit_record_1)
    print(f"First message audited with Firestore document ID: {doc_id_1}")

    doc_id_2 = persist_processed_message("message_audit_logs", audit_record_2)
    print(f"Second message audited with Firestore document ID: {doc_id_2}")
