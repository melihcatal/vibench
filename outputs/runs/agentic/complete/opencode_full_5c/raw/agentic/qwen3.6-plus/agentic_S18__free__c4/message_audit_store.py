import os
from datetime import datetime, timezone

from google.cloud import firestore

from messaging_models import AuditRecord, ConsumeResult, extract_text_from_payload


def store_audit_record(
    consume_result: ConsumeResult,
    processing_status: str = "processed",
    additional_metadata: dict | None = None,
    collection_name: str | None = None,
    project_id: str | None = None,
) -> AuditRecord:
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    collection_name = collection_name or os.environ.get(
        "FIRESTORE_AUDIT_COLLECTION", "message-audit-records"
    )

    payload_summary = extract_text_from_payload(consume_result.event.payload)
    if len(payload_summary) > 500:
        payload_summary = payload_summary[:500] + "..."

    metadata = additional_metadata or {}
    metadata["event_type"] = consume_result.event.event_type
    metadata["source"] = consume_result.event.source
    metadata["delivery_attempt"] = consume_result.delivery_attempt

    record = AuditRecord(
        record_id=f"audit-{consume_result.message_id}",
        message_id=consume_result.message_id,
        event_type=consume_result.event.event_type,
        source=consume_result.event.source,
        payload_summary=payload_summary,
        processing_status=processing_status,
        processed_at=datetime.now(timezone.utc).isoformat(),
        metadata=metadata,
    )

    db = firestore.Client(project=project_id)
    doc_ref = db.collection(collection_name).document(record.record_id)
    doc_ref.set(record.to_firestore_dict())

    return record


def lookup_audit_record(
    message_id: str,
    collection_name: str | None = None,
    project_id: str | None = None,
) -> AuditRecord | None:
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    collection_name = collection_name or os.environ.get(
        "FIRESTORE_AUDIT_COLLECTION", "message-audit-records"
    )

    db = firestore.Client(project=project_id)
    doc_ref = db.collection(collection_name).document(f"audit-{message_id}")
    doc = doc_ref.get()

    if doc.exists:
        return AuditRecord.from_firestore_dict(doc.to_dict())
    return None


def query_audit_records(
    event_type: str | None = None,
    processing_status: str | None = None,
    limit: int = 50,
    collection_name: str | None = None,
    project_id: str | None = None,
) -> list[AuditRecord]:
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    collection_name = collection_name or os.environ.get(
        "FIRESTORE_AUDIT_COLLECTION", "message-audit-records"
    )

    db = firestore.Client(project=project_id)
    collection = db.collection(collection_name)
    query = collection.limit(limit)

    if event_type:
        query = query.where("event_type", "==", event_type)
    if processing_status:
        query = query.where("processing_status", "==", processing_status)

    docs = query.stream()
    return [AuditRecord.from_firestore_dict(doc.to_dict()) for doc in docs]


if __name__ == "__main__":
    from messaging_models import EventMessage, ConsumeResult

    event = EventMessage.create(
        event_type="order.completed",
        source="order-service",
        payload={"order_id": "ORD-999", "total": 150.00},
    )
    consume = ConsumeResult(
        message_id="msg-audit-001",
        event=event,
        ack_id="ack-audit-001",
        delivery_attempt=1,
        received_at=datetime.now(timezone.utc).isoformat(),
    )
    record = store_audit_record(consume, processing_status="completed")
    print(record.to_dict())
