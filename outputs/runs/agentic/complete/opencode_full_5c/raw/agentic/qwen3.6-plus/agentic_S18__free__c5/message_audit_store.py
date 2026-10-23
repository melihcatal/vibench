import os
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from google.cloud import firestore
from messaging_models import normalize_payload


def get_firestore_client() -> firestore.Client:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-gcp-project")
    return firestore.Client(project=project_id)


def persist_message_record(
    message_data: Dict[str, Any],
    processing_result: Optional[Dict[str, Any]] = None,
    collection_name: str = "message_audit_log",
) -> Dict[str, Any]:
    db = get_firestore_client()

    payload = normalize_payload(message_data.get("data", message_data))

    record_id = message_data.get("message_id", str(uuid.uuid4()))
    record = {
        "record_id": record_id,
        "message_id": message_data.get("message_id", record_id),
        "event_type": message_data.get("attributes", {}).get("event_type", "unknown"),
        "payload": payload,
        "processing_result": processing_result,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "status": processing_result.get("status", "processed")
        if processing_result
        else "received",
        "provider": "google-cloud-firestore",
    }

    doc_ref = db.collection(collection_name).document(record_id)
    doc_ref.set(record)

    return {
        "record_id": record_id,
        "collection": collection_name,
        "status": "persisted",
        "provider": "google-cloud-firestore",
        "ingested_at": record["ingested_at"],
    }


def batch_persist_records(
    messages_with_results: List[Dict[str, Any]],
    collection_name: str = "message_audit_log",
) -> Dict[str, Any]:
    db = get_firestore_client()
    batch = db.batch()
    persisted_ids = []

    for item in messages_with_results:
        message_data = item.get("message", item)
        processing_result = item.get("processing_result")
        payload = normalize_payload(message_data.get("data", message_data))

        record_id = message_data.get("message_id", str(uuid.uuid4()))
        record = {
            "record_id": record_id,
            "message_id": message_data.get("message_id", record_id),
            "event_type": message_data.get("attributes", {}).get(
                "event_type", "unknown"
            ),
            "payload": payload,
            "processing_result": processing_result,
            "ingested_at": datetime.now(timezone.utc).isoformat(),
            "status": processing_result.get("status", "processed")
            if processing_result
            else "received",
            "provider": "google-cloud-firestore",
        }

        doc_ref = db.collection(collection_name).document(record_id)
        batch.set(doc_ref, record)
        persisted_ids.append(record_id)

    batch.commit()

    return {
        "persisted_count": len(persisted_ids),
        "record_ids": persisted_ids,
        "collection": collection_name,
        "status": "batch_persisted",
        "provider": "google-cloud-firestore",
    }


def query_message_records(
    query_filters: Dict[str, Any],
    collection_name: str = "message_audit_log",
    limit: int = 50,
) -> List[Dict[str, Any]]:
    db = get_firestore_client()
    collection_ref = db.collection(collection_name)

    query = collection_ref.limit(limit)

    for field, value in query_filters.items():
        query = query.where(field, "==", value)

    docs = query.stream()
    results = []

    for doc in docs:
        record = doc.to_dict()
        record["_document_id"] = doc.id
        results.append(record)

    return results


def get_message_record(
    record_id: str, collection_name: str = "message_audit_log"
) -> Optional[Dict[str, Any]]:
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(record_id)
    doc = doc_ref.get()

    if doc.exists:
        record = doc.to_dict()
        record["_document_id"] = doc.id
        return record
    return None


if __name__ == "__main__":
    sample_message = {
        "message_id": "msg_audit_001",
        "data": {"user_id": "u1", "action": "signup", "source": "web"},
        "attributes": {"event_type": "user.signup"},
    }
    sample_result = {"status": "processed", "safety": "safe", "language": "en"}
    result = persist_message_record(sample_message, processing_result=sample_result)
    print(json.dumps(result, indent=2))
