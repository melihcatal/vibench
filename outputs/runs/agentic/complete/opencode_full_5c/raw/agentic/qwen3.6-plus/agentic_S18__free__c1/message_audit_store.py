import os
from typing import Optional, List, Dict, Any

from google.cloud import firestore

from messaging_models import AuditRecord, EventMessage

GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
FIRESTORE_COLLECTION = os.environ.get("FIRESTORE_AUDIT_COLLECTION", "message_audit_log")


def get_firestore_client() -> firestore.Client:
    return firestore.Client(project=GOOGLE_CLOUD_PROJECT)


def persist_audit_record(
    audit_record: AuditRecord,
    collection_name: str = FIRESTORE_COLLECTION,
) -> str:
    client = get_firestore_client()
    collection_ref = client.collection(collection_name)

    doc_ref = collection_ref.document(audit_record.record_id)
    doc_ref.set(audit_record.to_dict())

    return audit_record.record_id


def persist_event_processing(
    event: EventMessage,
    processing_status: str = "processed",
    metadata: Optional[Dict[str, Any]] = None,
    summary: Optional[Any] = None,
    safety_check: Optional[Any] = None,
    translation: Optional[Any] = None,
    collection_name: str = FIRESTORE_COLLECTION,
) -> str:
    record = AuditRecord(
        message_id=event.event_id,
        event_type=event.event_type,
        processing_status=processing_status,
        metadata=metadata or {},
        summary=summary,
        safety_check=safety_check,
        translation=translation,
    )
    return persist_audit_record(record, collection_name=collection_name)


def get_audit_record(
    record_id: str,
    collection_name: str = FIRESTORE_COLLECTION,
) -> Optional[AuditRecord]:
    client = get_firestore_client()
    collection_ref = client.collection(collection_name)
    doc_ref = collection_ref.document(record_id)

    doc = doc_ref.get()
    if not doc.exists:
        return None

    data = doc.to_dict()
    return AuditRecord(
        record_id=doc.id,
        message_id=data.get("message_id", ""),
        event_type=data.get("event_type", ""),
        processing_status=data.get("processing_status", ""),
        processing_timestamp=data.get("processing_timestamp", ""),
        metadata=data.get("metadata", {}),
    )


def query_audit_records(
    event_type: Optional[str] = None,
    processing_status: Optional[str] = None,
    limit: int = 50,
    collection_name: str = FIRESTORE_COLLECTION,
) -> List[AuditRecord]:
    client = get_firestore_client()
    collection_ref = client.collection(collection_name)
    query = collection_ref.limit(limit)

    if event_type:
        query = query.where("event_type", "==", event_type)
    if processing_status:
        query = query.where("processing_status", "==", processing_status)

    query = query.order_by("processing_timestamp", direction=firestore.Query.DESCENDING)

    docs = query.stream()
    records = []
    for doc in docs:
        data = doc.to_dict()
        records.append(
            AuditRecord(
                record_id=doc.id,
                message_id=data.get("message_id", ""),
                event_type=data.get("event_type", ""),
                processing_status=data.get("processing_status", ""),
                processing_timestamp=data.get("processing_timestamp", ""),
                metadata=data.get("metadata", {}),
            )
        )

    return records


def update_audit_record(
    record_id: str,
    updates: Dict[str, Any],
    collection_name: str = FIRESTORE_COLLECTION,
) -> bool:
    client = get_firestore_client()
    collection_ref = client.collection(collection_name)
    doc_ref = collection_ref.document(record_id)

    doc_ref.update(updates)
    return True
