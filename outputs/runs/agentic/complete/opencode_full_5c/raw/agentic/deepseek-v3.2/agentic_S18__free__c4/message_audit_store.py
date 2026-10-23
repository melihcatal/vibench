import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from google.cloud import firestore
from google.cloud.firestore_v1 import FieldFilter


def store_processed_message(
    message_data: Dict[str, Any], collection_name: str = "message_audit"
) -> Dict[str, Any]:
    """Persist processed message records to Google Cloud Firestore for later lookup."""
    db = firestore.Client()

    audit_record = {
        "message_id": message_data.get("message_id"),
        "original_data": message_data.get("data"),
        "processed_at": datetime.utcnow(),
        "processing_status": message_data.get("status", "processed"),
        "metadata": {
            "source_topic": message_data.get("source_topic"),
            "consumer_id": message_data.get("consumer_id"),
            "processing_time_ms": message_data.get("processing_time_ms"),
            "attempt_count": message_data.get("attempt_count", 1),
        },
        "safety_check": message_data.get("safety_check"),
        "translation_info": message_data.get("translation_info"),
        "provider": "google-cloud-firestore",
    }

    if "publish_time" in message_data:
        audit_record["original_publish_time"] = message_data["publish_time"]

    doc_ref = db.collection(collection_name).document()
    doc_ref.set(audit_record)

    return {
        "audit_id": doc_ref.id,
        "message_id": audit_record["message_id"],
        "stored_at": audit_record["processed_at"].isoformat(),
        "collection": collection_name,
        "provider": "google-cloud-firestore",
    }


def batch_store_messages(
    messages: List[Dict[str, Any]], collection_name: str = "message_audit"
) -> Dict[str, Any]:
    """Batch store multiple processed messages."""
    db = firestore.Client()
    batch = db.batch()
    results = []

    for message in messages:
        audit_record = {
            "message_id": message.get("message_id"),
            "original_data": message.get("data"),
            "processed_at": datetime.utcnow(),
            "processing_status": message.get("status", "processed"),
            "metadata": {
                "source_topic": message.get("source_topic"),
                "consumer_id": message.get("consumer_id"),
                "processing_time_ms": message.get("processing_time_ms"),
                "attempt_count": message.get("attempt_count", 1),
            },
            "provider": "google-cloud-firestore",
        }

        if "publish_time" in message:
            audit_record["original_publish_time"] = message["publish_time"]

        if "safety_check" in message:
            audit_record["safety_check"] = message["safety_check"]

        if "translation_info" in message:
            audit_record["translation_info"] = message["translation_info"]

        doc_ref = db.collection(collection_name).document()
        batch.set(doc_ref, audit_record)
        results.append(
            {"audit_id": doc_ref.id, "message_id": audit_record["message_id"]}
        )

    batch.commit()

    return {
        "total_stored": len(results),
        "results": results,
        "collection": collection_name,
        "provider": "google-cloud-firestore",
    }


def lookup_message_by_id(
    message_id: str, collection_name: str = "message_audit"
) -> Dict[str, Any]:
    """Look up a message by its original message ID."""
    db = firestore.Client()

    query = db.collection(collection_name).where(
        filter=FieldFilter("message_id", "==", message_id)
    )
    docs = query.stream()

    results = []
    for doc in docs:
        data = doc.to_dict()
        data["audit_id"] = doc.id
        if "processed_at" in data and hasattr(data["processed_at"], "isoformat"):
            data["processed_at"] = data["processed_at"].isoformat()
        results.append(data)

    return {
        "message_id": message_id,
        "found_count": len(results),
        "results": results,
        "collection": collection_name,
        "provider": "google-cloud-firestore",
    }


def search_messages_by_time_range(
    start_time: datetime, end_time: datetime, collection_name: str = "message_audit"
) -> Dict[str, Any]:
    """Search for messages processed within a time range."""
    db = firestore.Client()

    query = (
        db.collection(collection_name)
        .where("processed_at", ">=", start_time)
        .where("processed_at", "<=", end_time)
        .order_by("processed_at")
    )

    docs = query.stream()

    results = []
    for doc in docs:
        data = doc.to_dict()
        data["audit_id"] = doc.id
        if "processed_at" in data and hasattr(data["processed_at"], "isoformat"):
            data["processed_at"] = data["processed_at"].isoformat()
        results.append(data)

    return {
        "time_range": {"start": start_time.isoformat(), "end": end_time.isoformat()},
        "found_count": len(results),
        "results": results,
        "collection": collection_name,
        "provider": "google-cloud-firestore",
    }


def search_messages_by_status(
    status: str, collection_name: str = "message_audit"
) -> Dict[str, Any]:
    """Search for messages by processing status."""
    db = firestore.Client()

    query = db.collection(collection_name).where(
        filter=FieldFilter("processing_status", "==", status)
    )
    docs = query.stream()

    results = []
    for doc in docs:
        data = doc.to_dict()
        data["audit_id"] = doc.id
        if "processed_at" in data and hasattr(data["processed_at"], "isoformat"):
            data["processed_at"] = data["processed_at"].isoformat()
        results.append(data)

    return {
        "status": status,
        "found_count": len(results),
        "results": results,
        "collection": collection_name,
        "provider": "google-cloud-firestore",
    }


def get_audit_statistics(
    collection_name: str = "message_audit", time_range_hours: int = 24
) -> Dict[str, Any]:
    """Get statistics about stored audit records."""
    db = firestore.Client()
    end_time = datetime.utcnow()
    start_time = end_time.replace(hour=0, minute=0, second=0, microsecond=0)

    query = (
        db.collection(collection_name)
        .where("processed_at", ">=", start_time)
        .where("processed_at", "<=", end_time)
    )

    docs = list(query.stream())

    status_counts = {}
    source_counts = {}
    total_processing_time = 0
    status_count = 0

    for doc in docs:
        data = doc.to_dict()

        status = data.get("processing_status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1

        source = data.get("metadata", {}).get("source_topic", "unknown")
        source_counts[source] = source_counts.get(source, 0) + 1

        processing_time = data.get("metadata", {}).get("processing_time_ms", 0)
        if processing_time:
            total_processing_time += processing_time
            status_count += 1

    avg_processing_time = (
        total_processing_time / status_count if status_count > 0 else 0
    )

    return {
        "time_range": {"start": start_time.isoformat(), "end": end_time.isoformat()},
        "total_records": len(docs),
        "status_distribution": status_counts,
        "source_distribution": source_counts,
        "average_processing_time_ms": avg_processing_time,
        "collection": collection_name,
        "provider": "google-cloud-firestore",
    }


def create_audit_indexes(collection_name: str = "message_audit") -> Dict[str, Any]:
    """Create recommended indexes for audit collection (documentation only - indexes must be created in Firestore console)."""
    return {
        "recommended_indexes": [
            {"fields": ["message_id"], "query_scopes": ["COLLECTION"]},
            {"fields": ["processed_at"], "query_scopes": ["COLLECTION"]},
            {"fields": ["processing_status"], "query_scopes": ["COLLECTION"]},
            {
                "fields": ["processed_at", "processing_status"],
                "query_scopes": ["COLLECTION"],
            },
        ],
        "collection": collection_name,
        "note": "Indexes must be created in Google Cloud Firestore console",
        "provider": "google-cloud-firestore",
    }


if __name__ == "__main__":
    sample_message = {
        "message_id": "test_msg_123",
        "data": {"user_id": "user_789", "action": "login"},
        "status": "processed",
        "source_topic": "event-topic",
        "consumer_id": "consumer_1",
        "processing_time_ms": 150,
    }

    store_result = store_processed_message(sample_message)
    print(f"Stored message: {json.dumps(store_result, indent=2)}")

    lookup_result = lookup_message_by_id("test_msg_123")
    print(f"Lookup result: {json.dumps(lookup_result, indent=2)}")
