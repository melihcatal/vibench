import os
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone

from identity_models import AuditEvent, serialize_audit_events, deserialize_audit_events


MONGODB_ATLAS_URI = os.environ.get(
    "MONGODB_ATLAS_URI", "mongodb+srv://user:pass@cluster0.mongodb.net/"
)
MONGODB_ATLAS_DB = os.environ.get("MONGODB_ATLAS_DB", "federated_identity")
MONGODB_ATLAS_COLLECTION = os.environ.get(
    "MONGODB_ATLAS_COLLECTION", "login_audit_events"
)


def get_mongo_client(
    uri: Optional[str] = None,
) -> Any:
    from pymongo import MongoClient

    mongo_uri = uri or MONGODB_ATLAS_URI
    return MongoClient(mongo_uri)


def persist_audit_event(
    event: AuditEvent,
    uri: Optional[str] = None,
    database: Optional[str] = None,
    collection: Optional[str] = None,
) -> str:
    client = get_mongo_client(uri)
    db_name = database or MONGODB_ATLAS_DB
    col_name = collection or MONGODB_ATLAS_COLLECTION

    doc = event.to_dict()
    doc["created_at"] = datetime.now(timezone.utc)
    doc["provider_store"] = "mongodb_atlas"

    db = client[db_name]
    result = db[col_name].insert_one(doc)

    return str(result.inserted_id)


def persist_audit_events_batch(
    events: List[AuditEvent],
    uri: Optional[str] = None,
    database: Optional[str] = None,
    collection: Optional[str] = None,
) -> List[str]:
    client = get_mongo_client(uri)
    db_name = database or MONGODB_ATLAS_DB
    col_name = collection or MONGODB_ATLAS_COLLECTION

    docs = []
    for event in events:
        doc = event.to_dict()
        doc["created_at"] = datetime.now(timezone.utc)
        doc["provider_store"] = "mongodb_atlas"
        docs.append(doc)

    db = client[db_name]
    result = db[col_name].insert_many(docs)

    return [str(oid) for oid in result.inserted_ids]


def query_audit_events(
    user_sub: Optional[str] = None,
    provider: Optional[str] = None,
    event_type: Optional[str] = None,
    status: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    limit: int = 100,
    uri: Optional[str] = None,
    database: Optional[str] = None,
    collection: Optional[str] = None,
) -> List[AuditEvent]:
    client = get_mongo_client(uri)
    db_name = database or MONGODB_ATLAS_DB
    col_name = collection or MONGODB_ATLAS_COLLECTION

    query: Dict[str, Any] = {}
    if user_sub:
        query["user_sub"] = user_sub
    if provider:
        query["provider"] = provider
    if event_type:
        query["event_type"] = event_type
    if status:
        query["status"] = status
    if start_time or end_time:
        time_filter: Dict[str, Any] = {}
        if start_time:
            time_filter["$gte"] = start_time
        if end_time:
            time_filter["$lte"] = end_time
        query["timestamp"] = time_filter

    db = client[db_name]
    cursor = db[col_name].find(query).sort("timestamp", -1).limit(limit)

    events = []
    for doc in cursor:
        doc.pop("_id", None)
        doc.pop("created_at", None)
        doc.pop("provider_store", None)
        events.append(AuditEvent.from_dict(doc))

    return events


def get_audit_event_by_id(
    event_id: str,
    uri: Optional[str] = None,
    database: Optional[str] = None,
    collection: Optional[str] = None,
) -> Optional[AuditEvent]:
    from bson import ObjectId

    client = get_mongo_client(uri)
    db_name = database or MONGODB_ATLAS_DB
    col_name = collection or MONGODB_ATLAS_COLLECTION

    db = client[db_name]
    try:
        doc = db[col_name].find_one({"_id": ObjectId(event_id)})
    except Exception:
        doc = db[col_name].find_one({"event_id": event_id})

    if not doc:
        return None

    doc.pop("_id", None)
    doc.pop("created_at", None)
    doc.pop("provider_store", None)
    return AuditEvent.from_dict(doc)


def update_audit_event(
    event_id: str,
    updates: Dict[str, Any],
    uri: Optional[str] = None,
    database: Optional[str] = None,
    collection: Optional[str] = None,
) -> bool:
    from bson import ObjectId

    client = get_mongo_client(uri)
    db_name = database or MONGODB_ATLAS_DB
    col_name = collection or MONGODB_ATLAS_COLLECTION

    updates["updated_at"] = datetime.now(timezone.utc)

    db = client[db_name]
    try:
        result = db[col_name].update_one(
            {"_id": ObjectId(event_id)},
            {"$set": updates},
        )
    except Exception:
        result = db[col_name].update_one(
            {"event_id": event_id},
            {"$set": updates},
        )

    return result.modified_count > 0


def create_audit_indexes(
    uri: Optional[str] = None,
    database: Optional[str] = None,
    collection: Optional[str] = None,
) -> List[str]:
    client = get_mongo_client(uri)
    db_name = database or MONGODB_ATLAS_DB
    col_name = collection or MONGODB_ATLAS_COLLECTION

    db = client[db_name]
    col = db[col_name]

    indexes_created = []

    col.create_index([("user_sub", 1), ("timestamp", -1)])
    indexes_created.append("user_sub_timestamp")

    col.create_index([("provider", 1), ("event_type", 1)])
    indexes_created.append("provider_event_type")

    col.create_index([("status", 1), ("timestamp", -1)])
    indexes_created.append("status_timestamp")

    col.create_index("event_id", unique=True)
    indexes_created.append("event_id_unique")

    col.create_index([("session_id", 1)])
    indexes_created.append("session_id")

    return indexes_created
