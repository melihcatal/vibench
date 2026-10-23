from google.cloud import firestore
import os
import datetime
from typing import Dict, Any

def store_message_record(project_id: str, collection_name: str, record_data: Dict[str, Any]) -> str:
    """Persists a processed message record to Google Firestore.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up.
    """
    db = firestore.Client(project=project_id)

    try:
        # Add a timestamp to the record
        record_data['timestamp'] = datetime.datetime.now(tz=datetime.timezone.utc)
        
        # Add a new document to the collection
        doc_ref = db.collection(collection_name).add(record_data)
        doc_id = doc_ref[1].id # doc_ref is a tuple (update_time, DocumentReference)
        print(f"Record stored successfully with ID: {doc_id}")
        return doc_id
    except Exception as e:
        print(f"Error storing record to Firestore: {e}")
        raise

if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    collection_name = "message_audit_logs"

    sample_record = {
        "message_id": "msg-abc-123",
        "processor": "message_safety_checker",
        "status": "processed",
        "payload_summary": "Checked text for safety. Result: TOXICITY=0.1",
        "original_payload_hash": "a1b2c3d4e5f6",
        "processing_time_ms": 150,
    }

    if not project_id:
        print("Please set GOOGLE_CLOUD_PROJECT_ID environment variable and ensure GOOGLE_APPLICATION_CREDENTIALS are set.")
    else:
        print("\n--- Storing sample message audit record ---")
        store_message_record(project_id, collection_name, sample_record)

        sample_record_2 = {
            "message_id": "msg-xyz-789",
            "processor": "payload_translator",
            "status": "translated",
            "original_text": "Hello",
            "translated_text": "Hola",
            "target_language": "es",
            "processing_time_ms": 50,
        }
        print("\n--- Storing another sample message audit record ---")
        store_message_record(project_id, collection_name, sample_record_2)
