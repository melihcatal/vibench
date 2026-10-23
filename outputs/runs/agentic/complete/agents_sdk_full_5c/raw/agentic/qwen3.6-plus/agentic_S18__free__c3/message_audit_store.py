"""Persist processed message records for later lookup.

Uses Google Cloud Firestore as the concrete external provider for document storage.
"""

import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from google.cloud import firestore

from messaging_models import EventMessage, AuditRecord, MessageResponse


GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "default-project")
FIRESTORE_AUDIT_COLLECTION = os.environ.get("FIRESTORE_AUDIT_COLLECTION", "message_audit_log")


def _get_firestore_client() -> firestore.Client:
    """Create and return a Google Cloud Firestore client."""
    return firestore.Client(project=GOOGLE_CLOUD_PROJECT)


def store_audit_record(
    audit_record: AuditRecord,
    collection_name: Optional[str] = None,
) -> MessageResponse:
    """Persist a single audit record to Google Cloud Firestore.

    Args:
        audit_record: The AuditRecord to store.
        collection_name: Optional Firestore collection name override.

    Returns:
        MessageResponse with the Firestore document reference details.
    """
    col_name = collection_name or FIRESTORE_AUDIT_COLLECTION

    try:
        db = _get_firestore_client()
        doc_ref = db.collection(col_name).document(audit_record.event_id)

        record_data = audit_record.to_dict()
        record_data["stored_at"] = datetime.utcnow().isoformat() + "Z"
        record_data["provider"] = "google-cloud-firestore"

        doc_ref.set(record_data)

        return MessageResponse(
            success=True,
            event_id=audit_record.event_id,
            message_id=doc_ref.id,
            details={
                "collection": col_name,
                "document_id": doc_ref.id,
                "provider": "google-cloud-firestore",
                "client_class": "firestore.Client",
            },
        )
    except Exception as exc:
        return MessageResponse(
            success=False,
            event_id=audit_record.event_id,
            error=str(exc),
            details={"collection": col_name, "provider": "google-cloud-firestore"},
        )


def store_audit_from_event(
    event: EventMessage,
    status: str = "processed",
    metadata: Optional[Dict[str, Any]] = None,
    collection_name: Optional[str] = None,
) -> MessageResponse:
    """Create and store an AuditRecord from an EventMessage.

    Args:
        event: The EventMessage that was processed.
        status: The processing status string.
        metadata: Optional additional metadata to store.
        collection_name: Optional Firestore collection name.

    Returns:
        MessageResponse from the store operation.
    """
    audit_record = AuditRecord(
        event_id=event.event_id,
        event_type=event.event_type,
        status=status,
        source=event.source,
        metadata=metadata or {},
    )
    return store_audit_record(audit_record, collection_name=collection_name)


def lookup_audit_record(
    event_id: str,
    collection_name: Optional[str] = None,
) -> MessageResponse:
    """Look up a stored audit record by event ID in Google Cloud Firestore.

    Args:
        event_id: The event ID to look up.
        collection_name: Optional Firestore collection name.

    Returns:
        MessageResponse with the audit record data or an error.
    """
    col_name = collection_name or FIRESTORE_AUDIT_COLLECTION

    try:
        db = _get_firestore_client()
        doc_ref = db.collection(col_name).document(event_id)
        doc = doc_ref.get()

        if not doc.exists:
            return MessageResponse(
                success=False,
                error=f"No audit record found for event_id: {event_id}",
                details={"collection": col_name, "provider": "google-cloud-firestore"},
            )

        return MessageResponse(
            success=True,
            event_id=event_id,
            details={
                "audit_record": doc.to_dict(),
                "collection": col_name,
                "provider": "google-cloud-firestore",
            },
        )
    except Exception as exc:
        return MessageResponse(
            success=False,
            error=str(exc),
            details={"collection": col_name, "provider": "google-cloud-firestore"},
        )


def batch_store_audit_records(
    audit_records: List[AuditRecord],
    collection_name: Optional[str] = None,
) -> List[MessageResponse]:
    """Store multiple audit records in a single Firestore batch write.

    Args:
        audit_records: List of AuditRecord objects to store.
        collection_name: Optional Firestore collection name.

    Returns:
        List of MessageResponse, one per record.
    """
    col_name = collection_name or FIRESTORE_AUDIT_COLLECTION

    try:
        db = _get_firestore_client()
        batch = db.batch()

        for record in audit_records:
            doc_ref = db.collection(col_name).document(record.event_id)
            record_data = record.to_dict()
            record_data["stored_at"] = datetime.utcnow().isoformat() + "Z"
            record_data["provider"] = "google-cloud-firestore"
            batch.set(doc_ref, record_data)

        batch.commit()

        results = []
        for record in audit_records:
            results.append(MessageResponse(
                success=True,
                event_id=record.event_id,
                details={
                    "collection": col_name,
                    "provider": "google-cloud-firestore",
                },
            ))
        return results
    except Exception as exc:
        results = []
        for record in audit_records:
            results.append(MessageResponse(
                success=False,
                event_id=record.event_id,
                error=str(exc),
                details={"collection": col_name, "provider": "google-cloud-firestore"},
            ))
        return results
