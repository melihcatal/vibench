from google.cloud import firestore
import os
import datetime

def persist_message_record(collection_name: str, message_data: dict) -> str:
    """Persists processed message records to Google Cloud Firestore."""
    db = firestore.Client()

    # Add a timestamp to the record
    message_data["timestamp"] = datetime.datetime.now(tz=datetime.timezone.utc)

    # Add the message data to the specified collection
    doc_ref = db.collection(collection_name).add(message_data)

    return doc_ref[1].id # Return the ID of the newly created document

if __name__ == "__main__":
    # This requires GOOGLE_APPLICATION_CREDENTIALS to be set up or run in a GCP environment.
    # For local testing, ensure your environment is authenticated.
    # Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    COLLECTION_NAME = os.getenv("FIRESTORE_COLLECTION_NAME", "message_audit_records")
    
    test_record = {
        "message_id": "pubsub-msg-12345",
        "event_type": "user_signup",
        "status": "processed",
        "payload_summary": "New user 'john.doe' registered.",
        "processing_service": "user-service",
    }
    
    try:
        document_id = persist_message_record(COLLECTION_NAME, test_record)
        print(f"Message record persisted with document ID: {document_id}")

        another_record = {
            "message_id": "pubsub-msg-67890",
            "event_type": "product_update",
            "status": "failed",
            "error": "Invalid product ID",
            "processing_service": "catalog-service",
        }
        document_id_2 = persist_message_record(COLLECTION_NAME, another_record)
        print(f"Another message record persisted with document ID: {document_id_2}")

    except Exception as e:
        print(f"Error persisting record to Firestore: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS is set and Firestore is enabled for your project.")
