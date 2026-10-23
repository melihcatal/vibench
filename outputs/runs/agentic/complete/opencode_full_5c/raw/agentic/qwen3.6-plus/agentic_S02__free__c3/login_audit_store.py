import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from identity_models import AuditEvent, AuditEventType


MONGODB_URI = os.environ.get(
    "MONGODB_URI",
    "mongodb+srv://<username>:<password>@cluster0.example.mongodb.net/?retryWrites=true&w=majority",
)
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "federated_login")
MONGODB_AUDIT_COLLECTION = os.environ.get("MONGODB_AUDIT_COLLECTION", "audit_events")


def get_mongo_client() -> MongoClient:
    return MongoClient(MONGODB_URI)


def get_audit_collection() -> Collection:
    client = get_mongo_client()
    db = client[MONGODB_DATABASE]
    return db[MONGODB_AUDIT_COLLECTION]


def store_audit_event(audit_event: AuditEvent) -> Dict[str, Any]:
    collection = get_audit_collection()

    document = audit_event.to_dict()
    document["_id"] = audit_event.event_id
    document["stored_at"] = datetime.now(timezone.utc).isoformat()
    document["provider"] = audit_event.provider or "mongodb_atlas"

    result = collection.insert_one(document)

    return {
        "success": True,
        "inserted_id": str(result.inserted_id),
        "event_id": audit_event.event_id,
        "provider": "mongodb_atlas",
        "collection": MONGODB_AUDIT_COLLECTION,
        "database": MONGODB_DATABASE,
    }


def store_batch_audit_events(events: List[AuditEvent]) -> Dict[str, Any]:
    collection = get_audit_collection()

    documents = []
    for event in events:
        doc = event.to_dict()
        doc["_id"] = event.event_id
        doc["stored_at"] = datetime.now(timezone.utc).isoformat()
        doc["provider"] = event.provider or "mongodb_atlas"
        documents.append(doc)

    result = collection.insert_many(documents)

    return {
        "success": True,
        "inserted_count": len(result.inserted_ids),
        "inserted_ids": [str(iid) for iid in result.inserted_ids],
        "provider": "mongodb_atlas",
        "collection": MONGODB_AUDIT_COLLECTION,
    }


def query_audit_events(
    user_id: Optional[str] = None,
    event_type: Optional[AuditEventType] = None,
    provider: Optional[str] = None,
    start_time: Optional[float] = None,
    end_time: Optional[float] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    collection = get_audit_collection()

    query_filter: Dict[str, Any] = {}
    if user_id:
        query_filter["user_id"] = user_id
    if event_type:
        query_filter["event_type"] = event_type.value
    if provider:
        query_filter["provider"] = provider
    if start_time:
        query_filter["timestamp"] = {"$gte": start_time}
    if end_time:
        if "timestamp" in query_filter:
            query_filter["timestamp"]["$lte"] = end_time
        else:
            query_filter["timestamp"] = {"$lte": end_time}

    cursor = collection.find(query_filter).sort("timestamp", -1).limit(limit)
    events = list(cursor)

    for event in events:
        event["_id"] = str(event["_id"])

    return events


def get_user_login_history(
    user_id: str,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    collection = get_audit_collection()

    cursor = collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)

    history = list(cursor)
    for event in history:
        event["_id"] = str(event["_id"])

    return history


def get_audit_statistics(
    hours: int = 24,
) -> Dict[str, Any]:
    collection = get_audit_collection()
    cutoff = time.time() - (hours * 60 * 60)

    pipeline = [
        {"$match": {"timestamp": {"$gte": cutoff}}},
        {
            "$group": {
                "_id": "$event_type",
                "count": {"$sum": 1},
                "providers": {"$addToSet": "$provider"},
            }
        },
        {"$sort": {"count": -1}},
    ]

    results = list(collection.aggregate(pipeline))

    event_type_stats = {}
    for result in results:
        event_type_stats[result["_id"]] = {
            "count": result["count"],
            "providers": result.get("providers", []),
        }

    total = sum(s["count"] for s in event_type_stats.values())

    return {
        "success": True,
        "provider": "mongodb_atlas",
        "time_range_hours": hours,
        "total_events": total,
        "event_type_breakdown": event_type_stats,
        "collection": MONGODB_AUDIT_COLLECTION,
        "database": MONGODB_DATABASE,
    }


def persist_federated_login_audit(
    audit_event: AuditEvent,
) -> Dict[str, Any]:
    return store_audit_event(audit_event)
