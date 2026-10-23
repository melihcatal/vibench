import os
from typing import Optional
from datetime import datetime, timezone
from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection

from identity_models import AuditRecord, AuditEventType


PROVIDER = "mongodb_atlas"
MONGODB_ATLAS_URI = os.environ.get(
    "MONGODB_ATLAS_URI", "mongodb+srv://user:pass@cluster0.example.mongodb.net/"
)
MONGODB_ATLAS_DATABASE = os.environ.get("MONGODB_ATLAS_DATABASE", "federated_identity")
MONGODB_ATLAS_AUDIT_COLLECTION = os.environ.get(
    "MONGODB_ATLAS_AUDIT_COLLECTION", "login_audit_events"
)


def get_mongo_client() -> MongoClient:
    return MongoClient(MONGODB_ATLAS_URI)


def get_audit_collection(
    client: Optional[MongoClient] = None,
    database: Optional[str] = None,
    collection: Optional[str] = None,
) -> Collection:
    mongo_client = client or get_mongo_client()
    db_name = database or MONGODB_ATLAS_DATABASE
    coll_name = collection or MONGODB_ATLAS_AUDIT_COLLECTION
    return mongo_client[db_name][coll_name]


def persist_audit_record(
    audit_record: AuditRecord,
    client: Optional[MongoClient] = None,
    database: Optional[str] = None,
    collection: Optional[str] = None,
) -> dict:
    coll = get_audit_collection(client=client, database=database, collection=collection)
    doc = audit_record.to_dict()
    doc["created_at"] = datetime.now(timezone.utc)
    doc["provider"] = PROVIDER
    doc["mongodb_atlas_collection"] = coll.name
    result = coll.insert_one(doc)
    return {
        "inserted_id": str(result.inserted_id),
        "event_id": audit_record.event_id,
        "collection": coll.name,
        "database": coll.database.name,
        "provider": PROVIDER,
    }


def persist_batch_audit_records(
    audit_records: list[AuditRecord],
    client: Optional[MongoClient] = None,
    database: Optional[str] = None,
    collection: Optional[str] = None,
) -> dict:
    coll = get_audit_collection(client=client, database=database, collection=collection)
    docs = []
    for record in audit_records:
        doc = record.to_dict()
        doc["created_at"] = datetime.now(timezone.utc)
        doc["provider"] = PROVIDER
        doc["mongodb_atlas_collection"] = coll.name
        docs.append(doc)
    result = coll.insert_many(docs)
    return {
        "inserted_ids": [str(oid) for oid in result.inserted_ids],
        "count": len(result.inserted_ids),
        "collection": coll.name,
        "database": coll.database.name,
        "provider": PROVIDER,
    }


def query_audit_records(
    user_id: Optional[str] = None,
    event_type: Optional[AuditEventType] = None,
    session_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    success: Optional[bool] = None,
    limit: int = 100,
    client: Optional[MongoClient] = None,
    database: Optional[str] = None,
    collection: Optional[str] = None,
) -> list[dict]:
    coll = get_audit_collection(client=client, database=database, collection=collection)
    query = {}
    if user_id:
        query["user_id"] = user_id
    if event_type:
        query["event_type"] = event_type.value
    if session_id:
        query["session_id"] = session_id
    if success is not None:
        query["success"] = success
    if start_date or end_date:
        date_range = {}
        if start_date:
            date_range["$gte"] = start_date
        if end_date:
            date_range["$lte"] = end_date
        query["timestamp"] = date_range
    cursor = coll.find(query).sort("timestamp", -1).limit(limit)
    return [
        {
            **doc,
            "_id": str(doc["_id"]),
        }
        for doc in cursor
    ]


def get_audit_record_by_id(
    event_id: str,
    client: Optional[MongoClient] = None,
    database: Optional[str] = None,
    collection: Optional[str] = None,
) -> Optional[dict]:
    coll = get_audit_collection(client=client, database=database, collection=collection)
    doc = coll.find_one({"event_id": event_id})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc


def get_audit_statistics(
    days: int = 30,
    client: Optional[MongoClient] = None,
    database: Optional[str] = None,
    collection: Optional[str] = None,
) -> dict:
    coll = get_audit_collection(client=client, database=database, collection=collection)
    start_date = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    pipeline = [
        {
            "$match": {
                "timestamp": {"$gte": start_date},
            }
        },
        {
            "$group": {
                "_id": "$event_type",
                "count": {"$sum": 1},
                "success_count": {
                    "$sum": {"$cond": [{"$eq": ["$success", True]}, 1, 0]}
                },
                "failure_count": {
                    "$sum": {"$cond": [{"$eq": ["$success", False]}, 1, 0]}
                },
            }
        },
    ]
    results = list(coll.aggregate(pipeline))
    event_stats = {}
    total_events = 0
    total_success = 0
    total_failure = 0
    for result in results:
        event_type = result["_id"]
        event_stats[event_type] = {
            "count": result["count"],
            "success_count": result["success_count"],
            "failure_count": result["failure_count"],
        }
        total_events += result["count"]
        total_success += result["success_count"]
        total_failure += result["failure_count"]
    unique_users = coll.distinct("user_id", {"timestamp": {"$gte": start_date}})
    unique_sessions = coll.distinct("session_id", {"timestamp": {"$gte": start_date}})
    return {
        "provider": PROVIDER,
        "mongodb_atlas_database": coll.database.name,
        "mongodb_atlas_collection": coll.name,
        "period_days": days,
        "summary": {
            "total_events": total_events,
            "total_successful": total_success,
            "total_failed": total_failure,
            "success_rate_pct": round(
                (total_success / total_events * 100) if total_events > 0 else 0, 2
            ),
            "unique_users": len(unique_users),
            "unique_sessions": len(unique_sessions),
        },
        "event_type_breakdown": event_stats,
    }


def create_ttl_index(
    days_to_expire: int = 90,
    client: Optional[MongoClient] = None,
    database: Optional[str] = None,
    collection: Optional[str] = None,
) -> str:
    coll = get_audit_collection(client=client, database=database, collection=collection)
    index_name = coll.create_index(
        [("created_at", 1)],
        expireAfterSeconds=days_to_expire * 86400,
        name="audit_ttl_index",
    )
    return index_name
