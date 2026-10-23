import os
from google.cloud import firestore
from messaging_models import ProcessedMessageResult

# Configure Google Cloud Firestore client
# Ensure GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS environment variables are set
def get_firestore_client():
    # Project ID is automatically detected from GOOGLE_CLOUD_PROJECT or credentials
    return firestore.Client()

def persist_processed_message(record: ProcessedMessageResult, collection_name: str = "message_audits") -> dict:
    """Persists processed message records to Google Firestore for later lookup."""
    db = get_firestore_client()

    try:
        doc_ref = db.collection(collection_name).document(record.message_id)
        doc_ref.set(record.to_dict())
        print(f"Successfully persisted message {record.message_id} to Firestore collection '{collection_name}'.")
        return {"success": True, "message_id": record.message_id, "collection": collection_name}
    except Exception as e:
        return {"success": False, "message_id": record.message_id, "error": f"Failed to persist record: {e}"}

def get_processed_message(message_id: str, collection_name: str = "message_audits") -> dict:
    """Retrieves a processed message record from Google Firestore."""
    db = get_firestore_client()

    try:
        doc_ref = db.collection(collection_name).document(message_id)
        doc = doc_ref.get()
        if doc.exists:
            print(f"Retrieved message {message_id} from Firestore.")
            return {"success": True, "message": doc.to_dict()}
        else:
            print(f"Message {message_id} not found in Firestore.")
            return {"success": False, "message": None, "error": "Not found"}
    except Exception as e:
        return {"success": False, "error": f"Failed to retrieve record: {e}"}

if __name__ == "__main__":
    # Example usage
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    # python message_audit_store.py

    test_record = ProcessedMessageResult(
        message_id="event-12345",
        status="SUCCESS",
        details="Message processed and delivered to downstream service."
    )

    print("\nPersisting test record...")
    persist_result = persist_processed_message(test_record)
    print(persist_result)

    print("\nRetrieving test record...")
    retrieve_result = get_processed_message("event-12345")
    print(retrieve_result)

    print("\nRetrieving non-existent record...")
    not_found_result = get_processed_message("non-existent-id")
    print(not_found_result)
