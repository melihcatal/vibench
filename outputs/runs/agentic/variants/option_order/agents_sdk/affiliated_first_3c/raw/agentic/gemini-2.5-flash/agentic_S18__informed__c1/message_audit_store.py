import os
import datetime
from typing import Dict, Any
from google.cloud import firestore

def persist_message_record(collection_name: str, record_data: Dict[str, Any], document_id: str = None, project_id: str = None) -> str:
    """
    Persists a processed message record to Google Cloud Firestore.
    If document_id is None, Firestore will auto-generate one.
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT env var not set.")

    db = firestore.Client(project=project_id)
    doc_ref = db.collection(collection_name).document(document_id) if document_id else db.collection(collection_name).document()

    # Add a timestamp for when the record was persisted
    record_data["audited_at"] = datetime.datetime.now(datetime.timezone.utc)

    doc_ref.set(record_data)
    print(f"Message record persisted to Firestore. Document ID: {doc_ref.id}")
    return doc_ref.id

if __name__ == "__main__":
    # Ensure GOOGLE_CLOUD_PROJECT is set in your environment
    if os.environ.get("GOOGLE_CLOUD_PROJECT"):
        sample_record = {
            "message_id": "msg-456",
            "event_type": "order_processed",
            "payload_summary": "Order for SKU-123, quantity 2, total $50",
            "processing_status": "completed",
            "consumer_service": "order-processor-v1"
        }
        
        # Persist with an auto-generated ID
        print("Persisting record with auto-generated ID:")
        auto_id = persist_message_record("message_audit_logs", sample_record)
        print(f"Auto-generated Document ID: {auto_id}")

        # Persist with a specific ID (e.g., using the message_id from the original event)
        sample_record_with_id = {
            "message_id": "msg-789",
            "event_type": "user_registered",
            "user_id": "user-abc",
            "processing_status": "completed"
        }
        print("\nPersisting record with specific ID:")
        specific_id = persist_message_record("message_audit_logs", sample_record_with_id, document_id="audit-msg-789")
        print(f"Specific Document ID: {specific_id}")

    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable to run this example.")
