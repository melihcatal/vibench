import os
from datetime import datetime, timezone
from pymongo import MongoClient, ASCENDING, DESCENDING

MONGODB_ATLAS_URI = os.environ.get(
    "MONGODB_ATLAS_URI", "mongodb+srv://<user>:<password>@cluster.mongodb.net/"
)
DATABASE_NAME = os.environ.get("MONGODB_AUDIT_DB", "messaging_audit")
COLLECTION_NAME = os.environ.get("MONGODB_AUDIT_COLLECTION", "processed_messages")

_client = MongoClient(MONGODB_ATLAS_URI)
_db = _client[DATABASE_NAME]
_collection = _db[COLLECTION_NAME]
_collection.create_index([("message_id", ASCENDING)])
_collection.create_index([("processed_at", DESCENDING)])


def persist_message_record(record: dict) -> str:
    doc = {
        **record,
        "processed_at": datetime.now(timezone.utc),
        "stored_at": datetime.now(timezone.utc).isoformat(),
    }
    result = _collection.insert_one(doc)
    return str(result.inserted_id)


def persist_batch_records(records: list[dict]) -> list[str]:
    docs = [
        {
            **r,
            "processed_at": datetime.now(timezone.utc),
            "stored_at": datetime.now(timezone.utc).isoformat(),
        }
        for r in records
    ]
    result = _collection.insert_many(docs)
    return [str(i) for i in result.inserted_ids]


def lookup_message(message_id: str) -> dict | None:
    doc = _collection.find_one({"message_id": message_id})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc


def lookup_messages_by_filter(filters: dict, limit: int = 50) -> list[dict]:
    cursor = _collection.find(filters).sort("processed_at", DESCENDING).limit(limit)
    results = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        results.append(doc)
    return results


def count_processed_messages() -> int:
    return _collection.count_documents({})
