import os
import datetime
from google.cloud import firestore

def store_audited_message(message_id: str, record_data: dict):
    """Persists processed message records for later lookup in Google Firestore.

    Args:
        message_id: A unique identifier for the message to be audited.
        record_data: A dictionary containing the data to store for the audited message.
                     This should include processing status, timestamp, any errors, etc.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable is typically used for authentication.
    # No explicit key loading needed if running in GCP environment or credentials are set up.
    try:
        db = firestore.Client()
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Firestore client. Ensure GOOGLE_APPLICATION_CREDENTIALS is set up. Error: {e}")

    collection_name = os.environ.get("FIRESTORE_AUDIT_COLLECTION", "message_audit_records")
    doc_ref = db.collection(collection_name).document(message_id)

    # Add a timestamp to the record data
    record_data["audited_at"] = datetime.datetime.now(datetime.timezone.utc)

    try:
        doc_ref.set(record_data)
        print(f"Audited message '{message_id}' to Firestore collection '{collection_name}'.")
    except Exception as e:
        print(f"Error storing message '{message_id}' to Firestore: {e}")

if __name__ == '__main__':
    # Example usage
    sample_message_id = "audit-msg-12345"
    sample_record = {
        "original_id": "event-abc-987",
        "status": "completed",
        "processor": "payload_translator",
        "output": {"translated_text": "Hello World"},
        "errors": []
    }
    store_audited_message(sample_message_id, sample_record)

    sample_message_id_fail = "audit-msg-fail-67890"
    sample_record_fail = {
        "original_id": "event-xyz-111",
        "status": "failed",
        "processor": "message_safety_check",
        "output": {},
        "errors": ["content_unsafe"]
    }
    store_audited_message(sample_message_id_fail, sample_record_fail)
