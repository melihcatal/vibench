import os
import json
from datetime import datetime
from typing import Dict, Optional
from google.cloud import firestore
from messaging_models import ProcessedMessage, EventMessage


def store_message_audit(processed_message: ProcessedMessage) -> str:
    """Persist processed message records to Google Cloud Firestore for later lookup."""
    client = firestore.Client(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project-id")
    )

    collection_name = os.environ.get("FIRESTORE_COLLECTION", "message_audit_logs")

    audit_data = processed_message.to_dict()

    doc_ref = client.collection(collection_name).document(processed_message.message_id)

    doc_ref.set(
        {
            **audit_data,
            "stored_at": datetime.utcnow().isoformat(),
            "searchable_customer_id": str(processed_message.event_message.customer_id),
            "searchable_event_type": processed_message.event_message.event_type,
            "searchable_timestamp": processed_message.event_message.timestamp,
        }
    )

    print(f"Stored audit record for message {processed_message.message_id}")
    return doc_ref.id


def get_message_audit(message_id: str) -> Optional[Dict]:
    """Retrieve message audit record from Firestore."""
    client = firestore.Client(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project-id")
    )

    collection_name = os.environ.get("FIRESTORE_COLLECTION", "message_audit_logs")

    doc_ref = client.collection(collection_name).document(message_id)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        print(f"No audit record found for message {message_id}")
        return None


def query_audit_records(
    customer_id: Optional[int] = None,
    event_type: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 100,
) -> list:
    """Query message audit records with filters."""
    client = firestore.Client(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project-id")
    )

    collection_name = os.environ.get("FIRESTORE_COLLECTION", "message_audit_logs")

    query = client.collection(collection_name)

    if customer_id is not None:
        query = query.where("searchable_customer_id", "==", str(customer_id))

    if event_type is not None:
        query = query.where("searchable_event_type", "==", event_type)

    if start_time is not None:
        query = query.where("searchable_timestamp", ">=", start_time.isoformat())

    if end_time is not None:
        query = query.where("searchable_timestamp", "<=", end_time.isoformat())

    query = query.order_by("searchable_timestamp", direction=firestore.Query.DESCENDING)
    query = query.limit(limit)

    results = query.stream()

    audit_records = []
    for doc in results:
        record = doc.to_dict()
        record["id"] = doc.id
        audit_records.append(record)

    print(f"Found {len(audit_records)} audit records")
    return audit_records


def store_processed_message_with_audit(
    event_message: EventMessage,
    message_id: str,
    success: bool,
    processing_time_ms: float,
    additional_info: Optional[Dict] = None,
) -> str:
    """Helper to create and store processed message with audit."""
    processed_msg = ProcessedMessage(
        message_id=message_id,
        event_message=event_message,
        processed_at=datetime.utcnow().isoformat(),
        success=success,
        processing_time_ms=processing_time_ms,
        additional_info=additional_info,
    )

    return store_message_audit(processed_msg)


if __name__ == "__main__":
    sample_event = EventMessage(
        event_type="order_created",
        customer_id=12345,
        timestamp="2024-01-15T10:30:00Z",
        payload={"order_id": "ORD-789", "amount": 99.99},
    )

    doc_id = store_processed_message_with_audit(
        event_message=sample_event,
        message_id="test-message-001",
        success=True,
        processing_time_ms=150.5,
        additional_info={"processor_version": "1.0.0"},
    )

    print(f"Stored audit record with ID: {doc_id}")

    retrieved = get_message_audit("test-message-001")
    if retrieved:
        print(f"Retrieved: {json.dumps(retrieved, indent=2)}")
