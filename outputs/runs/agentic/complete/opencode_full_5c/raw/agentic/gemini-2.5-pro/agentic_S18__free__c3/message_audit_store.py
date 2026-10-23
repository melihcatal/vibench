import os
from datetime import datetime, timezone
from google.cloud import firestore
from messaging_models import ProcessedMessage


def store_message_audit(processed_message: ProcessedMessage) -> str:
    """Persists a processed message record to Google Cloud Firestore."""
    db = firestore.Client(project=os.environ.get("GCP_PROJECT", "your-gcp-project-id"))

    collection_name = os.environ.get("FIRESTORE_COLLECTION", "message_audit")

    doc_ref = db.collection(collection_name).document(
        processed_message.original_message.message_id
    )

    audit_record = {
        "original_message_id": processed_message.original_message.message_id,
        "data": processed_message.original_message.data,
        "attributes": processed_message.original_message.attributes,
        "status": processed_message.status,
        "processed_at": firestore.SERVER_TIMESTAMP,
        "is_safe": processed_message.is_safe,
        "translation": processed_message.translation,
        "summary_included": bool(processed_message.summary),
    }

    doc_ref.set(audit_record)
    return doc_ref.id


if __name__ == "__main__":
    from messaging_models import Message

    # Requires authentication (e.g., gcloud auth application-default login)
    test_message = Message(
        data={"customer_id": "12345", "order_total": 99.99},
        attributes={"source_system": "test_script"},
    )

    processed = ProcessedMessage(
        original_message=test_message,
        status="SUCCESS",
        processed_at=datetime.now(timezone.utc).isoformat(),
        is_safe=True,
    )

    audit_id = store_message_audit(processed)
    print(f"Stored audit record with ID: {audit_id}")
