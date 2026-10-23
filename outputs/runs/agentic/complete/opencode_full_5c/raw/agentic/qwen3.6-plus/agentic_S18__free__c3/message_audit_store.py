import os
from typing import Optional
from google.cloud import firestore
from messaging_models import AuditRecord, EventMessage


GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "default-project")
FIRESTORE_DATABASE = os.environ.get("FIRESTORE_DATABASE", "(default)")
AUDIT_COLLECTION = os.environ.get("FIRESTORE_AUDIT_COLLECTION", "message_audit_log")


def get_firestore_client() -> firestore.Client:
    return firestore.Client(project=GCP_PROJECT_ID, database=FIRESTORE_DATABASE)


def store_audit_record(audit_data: dict) -> dict:
    client = get_firestore_client()
    collection_ref = client.collection(AUDIT_COLLECTION)

    record = AuditRecord(
        event_id=audit_data.get("event_id", ""),
        event_type=audit_data.get("event_type", ""),
        status=audit_data.get("status", "processed"),
        processing_result=audit_data.get("processing_result", {}),
        metadata=audit_data.get("metadata", {}),
    )

    try:
        doc_ref = collection_ref.document(record.record_id)
        doc_ref.set(record.to_dict())
        return {
            "success": True,
            "record_id": record.record_id,
            "document_path": doc_ref.path,
            "event_id": record.event_id,
        }
    except Exception as exc:
        return {
            "success": False,
            "record_id": record.record_id,
            "event_id": record.event_id,
            "error": str(exc),
        }


def store_event_audit(
    event_data: dict, status: str, processing_result: dict = None
) -> dict:
    event = EventMessage.from_dict(event_data)
    audit_data = {
        "event_id": event.event_id,
        "event_type": event.event_type,
        "status": status,
        "processing_result": processing_result or {},
        "metadata": {
            "source": event.source,
            "correlation_id": event.correlation_id,
            "timestamp": event.timestamp,
        },
    }
    return store_audit_record(audit_data)


def query_audit_records(
    event_id: str = None, event_type: str = None, status: str = None, limit: int = 50
) -> list:
    client = get_firestore_client()
    collection_ref = client.collection(AUDIT_COLLECTION)

    query = collection_ref

    if event_id:
        query = query.where("event_id", "==", event_id)
    if event_type:
        query = query.where("event_type", "==", event_type)
    if status:
        query = query.where("status", "==", status)

    query = query.order_by("processed_at", direction=firestore.Query.DESCENDING).limit(
        limit
    )

    try:
        docs = query.stream()
        results = []
        for doc in docs:
            record_data = doc.to_dict()
            record_data["document_id"] = doc.id
            results.append(record_data)
        return results
    except Exception as exc:
        return [{"error": str(exc)}]


def get_audit_record(record_id: str) -> Optional[dict]:
    client = get_firestore_client()
    collection_ref = client.collection(AUDIT_COLLECTION)

    try:
        doc_ref = collection_ref.document(record_id)
        doc = doc_ref.get()
        if doc.exists:
            record_data = doc.to_dict()
            record_data["document_id"] = doc.id
            return record_data
        return None
    except Exception:
        return None
