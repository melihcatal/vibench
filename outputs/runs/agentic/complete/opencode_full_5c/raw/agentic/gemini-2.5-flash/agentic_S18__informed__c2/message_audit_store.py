import os
from datetime import datetime
from google.cloud import firestore


def persist_message_record(
    collection_name: str, message_data: dict, document_id: str = None
) -> str:
    db = firestore.Client(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT")
    )  # GOOGLE_CLOUD_PROJECT is often set from GOOGLE_APPLICATION_CREDENTIALS

    if not db.project:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT environment variable not set or Firestore client not initialized correctly."
        )

    message_data["_audited_at"] = datetime.utcnow()

    if document_id:
        doc_ref = db.collection(collection_name).document(document_id)
        doc_ref.set(message_data)
        print(f"Message record updated with ID: {document_id}")
    else:
        doc_ref = db.collection(collection_name).add(message_data)
        document_id = doc_ref[1].id  # doc_ref is a tuple (update_time, document_ref)
        print(f"Message record persisted with ID: {document_id}")

    return document_id


if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable to your service account key file path
    # from your terminal: export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # from your terminal: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    # Example message record to store
    audit_record = {
        "original_message_id": "msg-abc-123",
        "topic": "user-events",
        "processed_status": "SUCCESS",
        "payload_summary": "User registered with email test@example.com",
        "processing_time_ms": 150,
    }

    # Replace 'message_audit_logs' with your desired Firestore collection name
    # Persist a new record
    new_doc_id = persist_message_record("message_audit_logs", audit_record)
    print(f"New document ID: {new_doc_id}")

    # Update an existing record (e.g., if you got a document_id back from a prior call)
    update_record = {
        "original_message_id": "msg-abc-123",
        "topic": "user-events",
        "processed_status": "UPDATED",
        "payload_summary": "User registration processed and updated.",
        "processing_time_ms": 200,
    }
    # To update, you'd typically retrieve the document ID first or have it from a previous operation.
    # For this example, we'll use the ID from the newly created document.
    persist_message_record("message_audit_logs", update_record, document_id=new_doc_id)
