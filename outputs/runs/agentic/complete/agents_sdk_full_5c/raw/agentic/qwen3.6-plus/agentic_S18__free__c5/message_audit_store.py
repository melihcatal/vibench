"""Persist processed message records for later lookup using Google Cloud Firestore.

Uses the google.cloud.firestore Client to store and retrieve message processing
audit records in a managed NoSQL document database for compliance and debugging.
"""

import os
from datetime import datetime, timezone
from typing import Any

from google.cloud.firestore import Client


DEFAULT_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "my-gcp-project")
DEFAULT_AUDIT_COLLECTION = os.getenv("FIRESTORE_AUDIT_COLLECTION", "message-audit")


def get_firestore_client(project_id: str | None = None) -> Client:
    """Create and return a Google Cloud Firestore client.

    Args:
        project_id: GCP project ID. Uses default if not provided.

    Returns:
        Configured firestore.Client instance.
    """
    pid = project_id or DEFAULT_PROJECT_ID
    return Client(project=pid)


def store_audit_record(
    record: dict[str, Any],
    collection_name: str | None = None,
    document_id: str | None = None,
    project_id: str | None = None,
    client: Client | None = None,
) -> str:
    """Store a processed message audit record in Google Cloud Firestore.

    Persists a dictionary record to a Firestore collection with a timestamp
    and optional document ID for later lookup.

    Args:
        record: Dictionary containing the audit record data.
        collection_name: Firestore collection name. Uses default if not provided.
        document_id: Optional document ID. Auto-generates if not provided.
        project_id: GCP project ID. Uses default if not provided.
        client: Optional pre-configured Firestore Client.

    Returns:
        The document ID of the stored record.

    Raises:
        Exception: If the Firestore write operation fails.
    """
    db = client or get_firestore_client(project_id)
    collection = collection_name or DEFAULT_AUDIT_COLLECTION

    audit_record = dict(record)
    audit_record["stored_at"] = datetime.now(timezone.utc).isoformat()
    audit_record["_version"] = 1

    if document_id:
        doc_ref = db.collection(collection).document(document_id)
        doc_ref.set(audit_record)
        return document_id
    else:
        doc_ref = db.collection(collection).add(audit_record)
        return doc_ref[1].id


def store_batch_audit_records(
    records: list[dict[str, Any]],
    collection_name: str | None = None,
    project_id: str | None = None,
    client: Client | None = None,
) -> list[str]:
    """Store multiple audit records in a batch Firestore write.

    Args:
        records: List of audit record dictionaries.
        collection_name: Firestore collection name.
        project_id: GCP project ID.
        client: Optional pre-configured Firestore Client.

    Returns:
        List of document IDs for the stored records.
    """
    db = client or get_firestore_client(project_id)
    collection = collection_name or DEFAULT_AUDIT_COLLECTION
    now = datetime.now(timezone.utc).isoformat()

    batch = db.batch()
    doc_ids = []

    for record in records:
        audit_record = dict(record)
        audit_record["stored_at"] = now
        audit_record["_version"] = 1

        doc_ref = db.collection(collection).document()
        batch.set(doc_ref, audit_record)
        doc_ids.append(doc_ref.id)

    batch.commit()
    return doc_ids


def lookup_audit_record(
    document_id: str,
    collection_name: str | None = None,
    project_id: str | None = None,
    client: Client | None = None,
) -> dict[str, Any] | None:
    """Look up a specific audit record by document ID in Google Cloud Firestore.

    Args:
        document_id: The document ID to look up.
        collection_name: Firestore collection name.
        project_id: GCP project ID.
        client: Optional pre-configured Firestore Client.

    Returns:
        Dictionary with the audit record data, or None if not found.
    """
    db = client or get_firestore_client(project_id)
    collection = collection_name or DEFAULT_AUDIT_COLLECTION

    doc_ref = db.collection(collection).document(document_id)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    return None


def query_audit_records(
    filters: dict[str, Any] | None = None,
    limit: int = 100,
    order_by: str = "stored_at",
    descending: bool = True,
    collection_name: str | None = None,
    project_id: str | None = None,
    client: Client | None = None,
) -> list[dict[str, Any]]:
    """Query audit records from Firestore with optional filters.

    Args:
        filters: Dictionary of field-value pairs to filter by.
        limit: Maximum number of records to return.
        order_by: Field name to order results by.
        descending: Whether to order in descending order.
        collection_name: Firestore collection name.
        project_id: GCP project ID.
        client: Optional pre-configured Firestore Client.

    Returns:
        List of matching audit record dictionaries.
    """
    db = client or get_firestore_client(project_id)
    collection = collection_name or DEFAULT_AUDIT_COLLECTION

    query = db.collection(collection)

    if filters:
        for field, value in filters.items():
            query = query.where(field, "==", value)

    query = query.order_by(order_by, direction=Client.DESCENDING if descending else Client.ASCENDING)
    query = query.limit(limit)

    docs = query.stream()
    return [doc.to_dict() for doc in docs]


def build_audit_record_from_event(
    event_id: str,
    event_type: str,
    source: str,
    status: str,
    payload: dict[str, Any] | None = None,
    processing_time_ms: int | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    """Build a standardized audit record dictionary from event metadata.

    Args:
        event_id: The event identifier.
        event_type: The event type classification.
        source: The event source identifier.
        status: Processing status (e.g., 'success', 'failed', 'dead_lettered').
        payload: Optional event payload to store.
        processing_time_ms: Optional processing duration in milliseconds.
        error: Optional error message if processing failed.

    Returns:
        Dictionary ready for storage in Firestore.
    """
    record = {
        "event_id": event_id,
        "event_type": event_type,
        "source": source,
        "status": status,
        "processed_at": datetime.now(timezone.utc).isoformat(),
    }

    if payload is not None:
        record["payload"] = payload
    if processing_time_ms is not None:
        record["processing_time_ms"] = processing_time_ms
    if error is not None:
        record["error"] = error

    return record


if __name__ == "__main__":
    record = build_audit_record_from_event(
        event_id="evt-12345",
        event_type="order.created",
        source="order-service",
        status="success",
        payload={"order_id": "ORD-999", "amount": 149.99},
        processing_time_ms=42,
    )
    doc_id = store_audit_record(record)
    print(f"Stored audit record with ID: {doc_id}")
