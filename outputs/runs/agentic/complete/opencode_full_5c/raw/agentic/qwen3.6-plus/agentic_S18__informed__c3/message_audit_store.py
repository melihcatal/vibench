import json
import os
from typing import Optional
from datetime import datetime, timezone
from pymongo import MongoClient, errors


MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME", "messaging_audit")
MONGODB_COLLECTION_NAME = os.environ.get(
    "MONGODB_COLLECTION_NAME", "processed_messages"
)

_client: Optional[MongoClient] = None


def get_mongo_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_ATLAS_URI, serverSelectionTimeoutMS=5000)
    return _client


def store_processed_message(
    message_id: str,
    event_type: str,
    source: str,
    payload: dict,
    processing_status: str,
    processing_metadata: Optional[dict] = None,
) -> dict:
    try:
        client = get_mongo_client()
        db = client[MONGODB_DB_NAME]
        collection = db[MONGODB_COLLECTION_NAME]

        document = {
            "message_id": message_id,
            "event_type": event_type,
            "source": source,
            "payload": payload,
            "processing_status": processing_status,
            "processing_metadata": processing_metadata or {},
            "stored_at": datetime.now(timezone.utc),
            "service": "MongoDB Atlas",
        }

        result = collection.insert_one(document)
        return {
            "success": True,
            "document_id": str(result.inserted_id),
            "message_id": message_id,
        }
    except errors.PyMongoError as exc:
        return {
            "success": False,
            "error": str(exc),
            "message_id": message_id,
        }


def lookup_processed_message(message_id: str) -> dict:
    try:
        client = get_mongo_client()
        db = client[MONGODB_DB_NAME]
        collection = db[MONGODB_COLLECTION_NAME]

        document = collection.find_one({"message_id": message_id})
        if document:
            document["_id"] = str(document["_id"])
            if "stored_at" in document:
                document["stored_at"] = document["stored_at"].isoformat()
            return {
                "success": True,
                "document": document,
            }
        return {
            "success": False,
            "error": "Message not found",
            "message_id": message_id,
        }
    except errors.PyMongoError as exc:
        return {
            "success": False,
            "error": str(exc),
            "message_id": message_id,
        }


def main():
    sample_record = {
        "message_id": "audit-msg-001",
        "event_type": "order.completed",
        "source": "payment-service",
        "payload": {"order_id": "ORD-789", "amount": 99.99},
        "processing_status": "completed",
        "processing_metadata": {"latency_ms": 120, "retries": 0},
    }
    result = store_processed_message(
        message_id=sample_record["message_id"],
        event_type=sample_record["event_type"],
        source=sample_record["source"],
        payload=sample_record["payload"],
        processing_status=sample_record["processing_status"],
        processing_metadata=sample_record["processing_metadata"],
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
