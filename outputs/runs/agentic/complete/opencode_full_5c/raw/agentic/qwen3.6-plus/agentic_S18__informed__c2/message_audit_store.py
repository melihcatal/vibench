import os
import json
from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo.collection import Collection


def get_audit_collection() -> Collection:
    uri = os.getenv("MONGODB_ATLAS_URI", "")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required")

    client = MongoClient(uri)
    db_name = os.getenv("MONGODB_DB_NAME", "messaging_audit")
    collection_name = os.getenv("MONGODB_COLLECTION_NAME", "processed_messages")
    return client[db_name][collection_name]


def store_message_record(
    event_id: str,
    event_type: str,
    source: str,
    payload: dict,
    processing_status: str,
    processed_at: str | None = None,
    metadata: dict | None = None,
) -> dict:
    collection = get_audit_collection()

    if processed_at is None:
        processed_at = datetime.now(timezone.utc).isoformat()

    record = {
        "event_id": event_id,
        "event_type": event_type,
        "source": source,
        "payload": payload,
        "processing_status": processing_status,
        "processed_at": processed_at,
        "metadata": metadata or {},
        "created_at": datetime.now(timezone.utc),
    }

    result = collection.insert_one(record)

    return {
        "record_id": str(result.inserted_id),
        "event_id": event_id,
        "status": "stored",
        "provider": "MongoDB Atlas",
    }


def store_batch_records(records: list[dict]) -> dict:
    collection = get_audit_collection()

    documents = []
    for rec in records:
        processed_at = rec.get("processed_at") or datetime.now(timezone.utc).isoformat()
        documents.append(
            {
                "event_id": rec["event_id"],
                "event_type": rec.get("event_type", ""),
                "source": rec.get("source", ""),
                "payload": rec.get("payload", {}),
                "processing_status": rec.get("processing_status", "unknown"),
                "processed_at": processed_at,
                "metadata": rec.get("metadata", {}),
                "created_at": datetime.now(timezone.utc),
            }
        )

    result = collection.insert_many(documents)

    return {
        "stored_count": len(result.inserted_ids),
        "record_ids": [str(rid) for rid in result.inserted_ids],
        "status": "stored",
        "provider": "MongoDB Atlas",
    }


def lookup_message_record(event_id: str) -> dict | None:
    collection = get_audit_collection()

    record = collection.find_one({"event_id": event_id})

    if record is None:
        return None

    record["_id"] = str(record["_id"])
    if "created_at" in record and record["created_at"]:
        record["created_at"] = record["created_at"].isoformat()

    return record


def query_records_by_status(
    processing_status: str,
    limit: int = 50,
) -> list[dict]:
    collection = get_audit_collection()

    cursor = collection.find({"processing_status": processing_status}).limit(limit)
    records = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        if "created_at" in doc and doc["created_at"]:
            doc["created_at"] = doc["created_at"].isoformat()
        records.append(doc)

    return records


if __name__ == "__main__":
    result = store_message_record(
        event_id="evt-audit-001",
        event_type="order.created",
        source="checkout-service",
        payload={"order_id": "ORD-54321", "amount": 149.99},
        processing_status="success",
        metadata={"processing_time_ms": 55, "handler_version": "2.1.0"},
    )
    print(json.dumps(result, indent=2, default=str))
