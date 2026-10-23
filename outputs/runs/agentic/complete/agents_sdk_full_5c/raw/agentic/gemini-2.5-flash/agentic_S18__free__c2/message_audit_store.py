import os
import json
import datetime
from google.cloud import firestore

def persist_processed_message_record(project_id: str, collection_name: str, record_data: dict) -> str:
    """Persists processed message records for later lookup using Google Cloud Firestore.
    Returns the ID of the newly created document.
    """
    # Initialize Firestore client
    # The project ID is usually inferred from the environment if running on GCP
    # or from GOOGLE_CLOUD_PROJECT environment variable.
    db = firestore.Client(project=project_id)

    # Get a reference to the collection
    collection_ref = db.collection(collection_name)

    # Add a new document with a generated ID
    # Firestore doesn't store datetime objects directly in JSON, but its client handles it.
    # Ensure datetime objects are properly handled if converting to/from JSON manually.
    
    # Convert any datetime objects in record_data to ISO format strings if they need to be strictly JSON serializable
    # or let Firestore client handle them. For simplicity here, assume datetime objects are fine.
    
    # Add a timestamp for when the record was stored
    record_data["stored_at"] = datetime.datetime.utcnow()

    doc_ref = collection_ref.add(record_data)
    return doc_ref[1].id # doc_ref is a tuple (update_time, document_reference)

if __name__ == '__main__':
    # Example usage:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    COLLECTION_NAME = os.getenv("FIRESTORE_COLLECTION_NAME", "message_audit_logs")
    
    sample_audit_record = {
        "original_message_id": "pubsub-msg-abc-123",
        "processing_status": "COMPLETED",
        "processed_by_service": "message-pipeline-v1",
        "processing_timestamp": datetime.datetime.utcnow().isoformat(),
        "summary_generated": True,
        "safety_checked": {"is_safe": True},
        "translation_attempted": {"target_lang": "es", "success": True},
        "payload_hash": "a1b2c3d4e5f6g7h8",
        "additional_metadata": {"user_agent": "curl/7.64.1"}
    }
    
    # print(f"Persisting audit record to Firestore collection {COLLECTION_NAME} in project {PROJECT_ID}...")
    # try:
    #     document_id = persist_processed_message_record(PROJECT_ID, COLLECTION_NAME, sample_audit_record)
    #     print(f"Audit record persisted with Document ID: {document_id}")
    # except Exception as e:
    #     print(f"Error persisting record: {e}")
