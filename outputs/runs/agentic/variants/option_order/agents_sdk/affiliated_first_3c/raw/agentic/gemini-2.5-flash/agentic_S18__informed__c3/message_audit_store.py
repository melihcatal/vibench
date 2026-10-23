from google.cloud import firestore
import os
from datetime import datetime
from typing import Dict, Any

def persist_message_record(project_id: str, collection_name: str, record: Dict[str, Any], doc_id: str = None) -> str:
    """Persists a processed message record to Google Cloud Firestore.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up.
    """
    if not project_id:
        raise ValueError("Google Cloud PROJECT_ID must be provided.")

    db = firestore.Client(project=project_id)
    
    # Add a timestamp to the record
    record["timestamp"] = firestore.SERVER_TIMESTAMP

    if doc_id:
        doc_ref = db.collection(collection_name).document(doc_id)
        doc_ref.set(record)
        print(f"Document {doc_id} in collection {collection_name} updated/created.")
    else:
        doc_ref = db.collection(collection_name).add(record)
        print(f"Document added with ID: {doc_ref[1].id} to collection {collection_name}.")
        doc_id = doc_ref[1].id
    
    return doc_id

if __name__ == '__main__':
    # Example usage
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    COLLECTION_NAME = os.getenv("FIRESTORE_COLLECTION_NAME", "message_audit_logs")
    
    if not PROJECT_ID:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        sample_record = {
            "message_id": "msg-abc-123",
            "status": "processed",
            "payload_summary": "Order 1001 placed by user 500.",
            "source_topic": "my-input-topic",
            "processing_details": {"steps": ["summarized", "translated"]}
        }
        
        try:
            generated_doc_id = persist_message_record(PROJECT_ID, COLLECTION_NAME, sample_record)
            print(f"\nRecord persisted with ID: {generated_doc_id}")

            # Example of updating/setting with a specific ID
            another_record = {
                "message_id": "msg-xyz-456",
                "status": "failed",
                "error_message": "Safety check failed.",
                "source_topic": "my-input-topic",
            }
            persist_message_record(PROJECT_ID, COLLECTION_NAME, another_record, doc_id="msg-xyz-456-log")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
