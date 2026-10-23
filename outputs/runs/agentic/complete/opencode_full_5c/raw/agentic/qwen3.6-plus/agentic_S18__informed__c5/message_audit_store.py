import os
from google.cloud import firestore
from messaging_models import AuditRecord


def get_firestore_client() -> firestore.Client:
    return firestore.Client()


def persist_audit_record(
    record: AuditRecord,
    collection_name: str = "message_audit_records",
) -> str:
    client = get_firestore_client()
    doc_ref = client.collection(collection_name).document(record.record_id)
    doc_ref.set(record.to_dict())
    return record.record_id


def get_audit_record(
    record_id: str,
    collection_name: str = "message_audit_records",
) -> dict:
    client = get_firestore_client()
    doc_ref = client.collection(collection_name).document(record_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return {}


def query_audit_records(
    message_id: str = None,
    processing_status: str = None,
    collection_name: str = "message_audit_records",
    limit: int = 50,
) -> list:
    client = get_firestore_client()
    query = client.collection(collection_name).limit(limit)
    if message_id:
        query = query.where("message_id", "==", message_id)
    if processing_status:
        query = query.where("processing_status", "==", processing_status)
    docs = query.stream()
    return [doc.to_dict() for doc in docs]


def store_processed_message(
    message_id: str,
    event_type: str,
    processing_status: str,
    safety_status: str = "",
    translation_status: str = "",
    summary: str = "",
    raw_payload: dict = None,
    metadata: dict = None,
    collection_name: str = "message_audit_records",
) -> str:
    record = AuditRecord(
        message_id=message_id,
        event_type=event_type,
        processing_status=processing_status,
        safety_status=safety_status,
        translation_status=translation_status,
        summary=summary,
        raw_payload=raw_payload or {},
        metadata=metadata or {},
    )
    return persist_audit_record(record, collection_name)


if __name__ == "__main__":
    record_id = store_processed_message(
        message_id="evt-001",
        event_type="user.created",
        processing_status="completed",
        safety_status="safe",
        translation_status="translated",
        summary="User signup processed successfully",
        raw_payload={"user_id": "12345", "email": "user@example.com"},
        metadata={"region": "us-east1"},
    )
    print(f"Stored audit record: {record_id}")
    retrieved = get_audit_record(record_id)
    print(retrieved)
