import os
from google.cloud import firestore
import datetime
import json

def store_message_audit_record(project_id: str, collection_name: str, message_id: str, record_data: dict) -> dict:
    """Persists processed message records to Google Cloud Firestore for later lookup."""
    db = firestore.Client(project=project_id)

    # Add a timestamp to the record
    record_data["audit_timestamp"] = datetime.datetime.now(datetime.timezone.utc)

    # Create a document reference with the message_id as the document ID
    doc_ref = db.collection(collection_name).document(message_id)

    # Set the data, merging if the document already exists
    doc_ref.set(record_data, merge=True)

    print(f"Stored audit record for message ID '{message_id}' in collection '{collection_name}'.")

    # Retrieve the stored document to confirm and return its snapshot
    stored_doc = doc_ref.get()
    if stored_doc.exists:
        print(f"Retrieved stored data: {json.dumps(stored_doc.to_dict(), indent=2, default=str)}")
        return stored_doc.to_dict()
    else:
        print(f"Failed to retrieve document for message ID '{message_id}'.")
        return {}

if __name__ == '__main__':
    # Example usage:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    FIRESTORE_COLLECTION = "message_audit_logs" # Name of your Firestore collection

    if not PROJECT_ID:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
    else:
        test_message_id = "msg-processed-abc-123"
        audit_data = {
            "original_message_id": test_message_id,
            "processor_service": "message_pipeline_v1",
            "status": "COMPLETED",
            "processed_payload_summary": {"items_processed": 5, "total_cost": 123.45},
            "translation_status": "translated_to_es",
            "safety_check_status": "safe",
        }

        store_message_audit_record(PROJECT_ID, FIRESTORE_COLLECTION, test_message_id, audit_data)

        test_message_id_2 = "msg-failed-xyz-456"
        audit_data_2 = {
            "original_message_id": test_message_id_2,
            "processor_service": "message_pipeline_v1",
            "status": "FAILED",
            "error_details": "Database write error",
            "dlq_entry_id": "dlq-msg-987"
        }
        store_message_audit_record(PROJECT_ID, FIRESTORE_COLLECTION, test_message_id_2, audit_data_2)
