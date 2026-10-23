import os
import json
from datetime import datetime, timezone
from typing import Any

from google.cloud import firestore

from messaging_models import AuditRecord


GOOGLE_CLOUD_PROJECT_ENV = "GCP_PROJECT_ID"
FIRESTORE_DATABASE_ENV = "FIRESTORE_DATABASE_ID"
AUDIT_COLLECTION = "message_audit_records"


def _get_firestore_client() -> firestore.Client:
    project_id = os.environ.get(GOOGLE_CLOUD_PROJECT_ENV)
    database_id = os.environ.get(FIRESTORE_DATABASE_ENV)

    kwargs = {}
    if project_id:
        kwargs["project"] = project_id
    if database_id:
        kwargs["database"] = database_id

    return firestore.Client(**kwargs)


def persist_audit_record(record: AuditRecord) -> dict[str, Any]:
    db = _get_firestore_client()
    collection_ref = db.collection(AUDIT_COLLECTION)

    doc_data = record.to_dict()
    doc_data["stored_at"] = datetime.now(timezone.utc).isoformat()

    doc_ref = collection_ref.document(record.record_id)
    doc_ref.set(doc_data)

    return {
        "record_id": record.record_id,
        "status": "persisted",
        "collection": AUDIT_COLLECTION,
        "document_path": doc_ref.path,
        "provider": "google-cloud-firestore",
    }


def store_processing_result(
    event_id: str,
    message_id: str,
    processing_status: str,
    processing_result: dict[str, Any],
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    record = AuditRecord(
        event_id=event_id,
        message_id=message_id,
        processing_status=processing_status,
        processing_result=processing_result,
        metadata=metadata or {},
    )
    return persist_audit_record(record)


def lookup_audit_record(record_id: str) -> dict[str, Any]:
    db = _get_firestore_client()
    collection_ref = db.collection(AUDIT_COLLECTION)
    doc_ref = collection_ref.document(record_id)

    doc = doc_ref.get()

    if not doc.exists:
        return {
            "record_id": record_id,
            "status": "not_found",
            "provider": "google-cloud-firestore",
        }

    data = doc.to_dict()
    data["record_id"] = doc.id
    data["status"] = "found"
    return data


def query_audit_records_by_event(event_id: str) -> list[dict[str, Any]]:
    db = _get_firestore_client()
    collection_ref = db.collection(AUDIT_COLLECTION)

    query = collection_ref.where("event_id", "==", event_id).order_by("processed_at")
    docs = query.stream()

    results = []
    for doc in docs:
        data = doc.to_dict()
        data["record_id"] = doc.id
        results.append(data)

    return results


def query_audit_records_by_status(status: str, limit: int = 50) -> list[dict[str, Any]]:
    db = _get_firestore_client()
    collection_ref = db.collection(AUDIT_COLLECTION)

    query = (
        collection_ref.where("processing_status", "==", status)
        .limit(limit)
        .order_by("processed_at")
    )
    docs = query.stream()

    results = []
    for doc in docs:
        data = doc.to_dict()
        data["record_id"] = doc.id
        results.append(data)

    return results


if __name__ == "__main__":
    sample_record = AuditRecord(
        event_id="evt-test-001",
        message_id="msg-test-001",
        processing_status="completed",
        processing_result={"summary": "test result"},
        metadata={"source": "cli"},
    )
    result = persist_audit_record(sample_record)
    print(json.dumps(result, indent=2))
