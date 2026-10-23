from datetime import datetime, timezone
from typing import Mapping

from pymongo import MongoClient


MONGODB_COLLECTION = "message_audit_records"


def store_audit_record(uri: str, record: Mapping[str, object]) -> Mapping[str, object]:
    client = MongoClient(uri)
    db = client.get_default_database()
    collection = db[MONGODB_COLLECTION]
    payload = dict(record)
    payload.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    result = collection.insert_one(payload)
    return {"provider": "MongoDB Atlas", "inserted_id": str(result.inserted_id), "collection": MONGODB_COLLECTION}
