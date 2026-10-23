import os
import json
from datetime import datetime, timezone
from pymongo import MongoClient
from messaging_models import PubSubEvent, ConsumeResult


MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.environ.get("MONGODB_AUDIT_DB", "messaging_audit")
COLLECTION_NAME = os.environ.get("MONGODB_AUDIT_COLLECTION", "processed_messages")


def get_mongo_client() -> MongoClient:
    return MongoClient(MONGODB_ATLAS_URI)


def persist_message_record(
    result: ConsumeResult,
    processing_summary: dict | None = None,
    safety_check: dict | None = None,
    translation: dict | None = None,
) -> dict:
    event = result.to_event()
    client = get_mongo_client()
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    record = {
        "message_id": result.message_id,
        "event_id": event.event_id if event else None,
        "event_type": event.event_type if event else None,
        "source": event.source if event else None,
        "timestamp": event.timestamp
        if event
        else datetime.now(timezone.utc).isoformat(),
        "payload": event.payload if event else {},
        "attributes": event.attributes if event else {},
        "delivery_attempt": result.delivery_attempt,
        "acknowledged": result.acknowledged,
        "processing_summary": processing_summary,
        "safety_check": safety_check,
        "translation": translation,
        "stored_at": datetime.now(timezone.utc).isoformat(),
        "service": "MongoDB Atlas",
    }

    inserted = collection.insert_one(record)

    return {
        "record_id": str(inserted.inserted_id),
        "message_id": result.message_id,
        "event_id": record["event_id"],
        "database": DATABASE_NAME,
        "collection": COLLECTION_NAME,
        "stored_at": record["stored_at"],
        "service": "MongoDB Atlas",
    }


def lookup_message_record(message_id: str) -> dict | None:
    client = get_mongo_client()
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    record = collection.find_one({"message_id": message_id})
    if record:
        record["_id"] = str(record["_id"])
    return record


if __name__ == "__main__":
    from messaging_models import ConsumeResult, PubSubEvent

    evt = PubSubEvent(
        event_type="order.created",
        source="order-service",
        payload={"order_id": "ORD-12345", "amount": 99.99},
    )
    cr = ConsumeResult(message_id="msg-audit-001", event=evt, acknowledged=True)
    audit = persist_message_record(cr, processing_summary={"summary": "Order created"})
    print(json.dumps(audit, indent=2))
