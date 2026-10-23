import os
from datetime import datetime, timezone
from typing import Optional
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import PyMongoError
from identity_models import AuditEvent


def get_mongo_client() -> MongoClient:
    uri = os.environ.get("MONGODB_ATLAS_URI", "")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required")
    client = MongoClient(uri)
    return client


def store_audit_event(
    event: AuditEvent,
    database: str = "federated_identity",
    collection: str = "audit_events",
) -> str:
    client = get_mongo_client()
    db = client[database]
    col = db[collection]
    doc = event.to_dict()
    doc["created_at"] = datetime.now(timezone.utc)
    doc["updated_at"] = datetime.now(timezone.utc)
    result = col.insert_one(doc)
    client.close()
    return str(result.inserted_id)


def store_audit_events_batch(
    events: list[AuditEvent],
    database: str = "federated_identity",
    collection: str = "audit_events",
) -> list[str]:
    client = get_mongo_client()
    db = client[database]
    col = db[collection]
    docs = []
    for event in events:
        doc = event.to_dict()
        doc["created_at"] = datetime.now(timezone.utc)
        doc["updated_at"] = datetime.now(timezone.utc)
        docs.append(doc)
    result = col.insert_many(docs)
    client.close()
    return [str(id_) for id_ in result.inserted_ids]


def query_audit_events(
    user_sub: Optional[str] = None,
    provider: Optional[str] = None,
    event_type: Optional[str] = None,
    success: Optional[bool] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 100,
    database: str = "federated_identity",
    collection: str = "audit_events",
) -> list[dict]:
    client = get_mongo_client()
    db = client[database]
    col = db[collection]
    query = {}
    if user_sub:
        query["user_sub"] = user_sub
    if provider:
        query["provider"] = provider
    if event_type:
        query["event_type"] = event_type
    if success is not None:
        query["success"] = success
    if start_time or end_time:
        time_query = {}
        if start_time:
            time_query["$gte"] = start_time.isoformat()
        if end_time:
            time_query["$lte"] = end_time.isoformat()
        query["timestamp"] = time_query
    cursor = col.find(query).sort("timestamp", DESCENDING).limit(limit)
    results = list(cursor)
    client.close()
    return results


def create_audit_indexes(
    database: str = "federated_identity",
    collection: str = "audit_events",
) -> list[str]:
    client = get_mongo_client()
    db = client[database]
    col = db[collection]
    indexes_created = []
    try:
        col.create_index([("user_sub", ASCENDING), ("timestamp", DESCENDING)])
        indexes_created.append("user_sub_timestamp")
    except PyMongoError:
        pass
    try:
        col.create_index([("provider", ASCENDING), ("event_type", ASCENDING)])
        indexes_created.append("provider_event_type")
    except PyMongoError:
        pass
    try:
        col.create_index([("timestamp", DESCENDING)])
        indexes_created.append("timestamp_desc")
    except PyMongoError:
        pass
    try:
        col.create_index([("event_id", ASCENDING)], unique=True)
        indexes_created.append("event_id_unique")
    except PyMongoError:
        pass
    client.close()
    return indexes_created


def get_audit_statistics(
    database: str = "federated_identity",
    collection: str = "audit_events",
    days: int = 30,
) -> dict:
    client = get_mongo_client()
    db = client[database]
    col = db[collection]
    cutoff = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    cutoff = cutoff.replace(day=cutoff.day - days)
    pipeline = [
        {"$match": {"timestamp": {"$gte": cutoff.isoformat()}}},
        {
            "$group": {
                "_id": "$provider",
                "total_events": {"$sum": 1},
                "successful": {"$sum": {"$cond": [{"$eq": ["$success", True]}, 1, 0]}},
                "failed": {"$sum": {"$cond": [{"$eq": ["$success", False]}, 1, 0]}},
                "unique_users": {"$addToSet": "$user_sub"},
            }
        },
    ]
    results = list(col.aggregate(pipeline))
    stats = {}
    for r in results:
        provider = r["_id"] or "unknown"
        stats[provider] = {
            "total_events": r["total_events"],
            "successful": r["successful"],
            "failed": r["failed"],
            "unique_users": len(r["unique_users"]),
        }
    client.close()
    return {
        "provider": "mongodb_atlas",
        "database": database,
        "collection": collection,
        "period_days": days,
        "statistics": stats,
    }
