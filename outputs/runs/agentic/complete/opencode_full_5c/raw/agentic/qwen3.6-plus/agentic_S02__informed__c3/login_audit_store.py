import os
import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from identity_models import AuditEvent


MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "mongodb://localhost:27017")
MONGODB_ATLAS_DB_NAME = os.environ.get("MONGODB_ATLAS_DB_NAME", "federated_login")
MONGODB_ATLAS_COLLECTION_NAME = os.environ.get(
    "MONGODB_ATLAS_COLLECTION_NAME", "audit_events"
)


def get_mongo_client(uri: Optional[str] = None) -> MongoClient:
    if not uri:
        uri = MONGODB_ATLAS_URI
    return MongoClient(uri)


def store_audit_event(
    audit_event: Dict[str, Any],
    db_name: Optional[str] = None,
    collection_name: Optional[str] = None,
    uri: Optional[str] = None,
) -> Dict[str, Any]:
    if not db_name:
        db_name = MONGODB_ATLAS_DB_NAME
    if not collection_name:
        collection_name = MONGODB_ATLAS_COLLECTION_NAME

    client = get_mongo_client(uri)
    db = client[db_name]
    collection = db[collection_name]

    document = {
        "event_id": audit_event.get("event_id", ""),
        "event_type": audit_event.get("event_type", ""),
        "timestamp": datetime.fromtimestamp(
            audit_event.get("timestamp", time.time()), tz=timezone.utc
        ),
        "user_sub": audit_event.get("user_sub", ""),
        "provider": audit_event.get("provider", ""),
        "ip_address": audit_event.get("ip_address", ""),
        "user_agent": audit_event.get("user_agent", ""),
        "success": audit_event.get("success", True),
        "details": audit_event.get("details", {}),
        "stored_at": datetime.now(timezone.utc),
    }

    try:
        result = collection.insert_one(document)
        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "event_id": document["event_id"],
            "provider": "mongodb_atlas",
            "database": db_name,
            "collection": collection_name,
            "stored_at": document["stored_at"].isoformat(),
        }
    except PyMongoError as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "mongodb_atlas",
            "database": db_name,
            "collection": collection_name,
        }
    finally:
        client.close()


def store_audit_events_batch(
    audit_events: List[Dict[str, Any]],
    db_name: Optional[str] = None,
    collection_name: Optional[str] = None,
    uri: Optional[str] = None,
) -> Dict[str, Any]:
    if not db_name:
        db_name = MONGODB_ATLAS_DB_NAME
    if not collection_name:
        collection_name = MONGODB_ATLAS_COLLECTION_NAME

    client = get_mongo_client(uri)
    db = client[db_name]
    collection = db[collection_name]

    documents = []
    for event in audit_events:
        document = {
            "event_id": event.get("event_id", ""),
            "event_type": event.get("event_type", ""),
            "timestamp": datetime.fromtimestamp(
                event.get("timestamp", time.time()), tz=timezone.utc
            ),
            "user_sub": event.get("user_sub", ""),
            "provider": event.get("provider", ""),
            "ip_address": event.get("ip_address", ""),
            "user_agent": event.get("user_agent", ""),
            "success": event.get("success", True),
            "details": event.get("details", {}),
            "stored_at": datetime.now(timezone.utc),
        }
        documents.append(document)

    try:
        result = collection.insert_many(documents)
        return {
            "success": True,
            "inserted_count": len(result.inserted_ids),
            "inserted_ids": [str(oid) for oid in result.inserted_ids],
            "provider": "mongodb_atlas",
            "database": db_name,
            "collection": collection_name,
            "stored_at": datetime.now(timezone.utc).isoformat(),
        }
    except PyMongoError as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "mongodb_atlas",
            "database": db_name,
            "collection": collection_name,
        }
    finally:
        client.close()


def query_audit_events(
    user_sub: Optional[str] = None,
    provider: Optional[str] = None,
    event_type: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 100,
    db_name: Optional[str] = None,
    collection_name: Optional[str] = None,
    uri: Optional[str] = None,
) -> Dict[str, Any]:
    if not db_name:
        db_name = MONGODB_ATLAS_DB_NAME
    if not collection_name:
        collection_name = MONGODB_ATLAS_COLLECTION_NAME

    client = get_mongo_client(uri)
    db = client[db_name]
    collection = db[collection_name]

    query_filter: Dict[str, Any] = {}
    if user_sub:
        query_filter["user_sub"] = user_sub
    if provider:
        query_filter["provider"] = provider
    if event_type:
        query_filter["event_type"] = event_type
    if start_time or end_time:
        time_filter = {}
        if start_time:
            time_filter["$gte"] = start_time
        if end_time:
            time_filter["$lte"] = end_time
        query_filter["timestamp"] = time_filter

    try:
        cursor = collection.find(query_filter).sort("timestamp", -1).limit(limit)
        events = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            doc["timestamp"] = (
                doc["timestamp"].isoformat() if doc.get("timestamp") else None
            )
            doc["stored_at"] = (
                doc["stored_at"].isoformat() if doc.get("stored_at") else None
            )
            events.append(doc)

        return {
            "success": True,
            "events": events,
            "count": len(events),
            "provider": "mongodb_atlas",
            "database": db_name,
            "collection": collection_name,
            "queried_at": datetime.now(timezone.utc).isoformat(),
        }
    except PyMongoError as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "mongodb_atlas",
            "database": db_name,
            "collection": collection_name,
        }
    finally:
        client.close()


def get_audit_statistics(
    db_name: Optional[str] = None,
    collection_name: Optional[str] = None,
    uri: Optional[str] = None,
) -> Dict[str, Any]:
    if not db_name:
        db_name = MONGODB_ATLAS_DB_NAME
    if not collection_name:
        collection_name = MONGODB_ATLAS_COLLECTION_NAME

    client = get_mongo_client(uri)
    db = client[db_name]
    collection = db[collection_name]

    try:
        total_count = collection.count_documents({})
        success_count = collection.count_documents({"success": True})
        failure_count = collection.count_documents({"success": False})

        provider_pipeline = [
            {"$group": {"_id": "$provider", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
        ]
        provider_stats = list(collection.aggregate(provider_pipeline))

        event_type_pipeline = [
            {"$group": {"_id": "$event_type", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
        ]
        event_type_stats = list(collection.aggregate(event_type_pipeline))

        return {
            "success": True,
            "total_events": total_count,
            "success_count": success_count,
            "failure_count": failure_count,
            "success_rate": success_count / total_count if total_count > 0 else 0,
            "by_provider": [
                {"provider": s["_id"], "count": s["count"]} for s in provider_stats
            ],
            "by_event_type": [
                {"event_type": s["_id"], "count": s["count"]} for s in event_type_stats
            ],
            "provider": "mongodb_atlas",
            "database": db_name,
            "collection": collection_name,
            "queried_at": datetime.now(timezone.utc).isoformat(),
        }
    except PyMongoError as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "mongodb_atlas",
            "database": db_name,
            "collection": collection_name,
        }
    finally:
        client.close()


if __name__ == "__main__":
    sample_event = {
        "event_id": "evt-001",
        "event_type": "token_exchange",
        "timestamp": time.time(),
        "user_sub": "auth0|12345",
        "provider": "auth0",
        "ip_address": "192.168.1.1",
        "user_agent": "Mozilla/5.0",
        "success": True,
        "details": {"flow_type": "pkce"},
    }
    result = store_audit_event(sample_event)
    print(json.dumps(result, indent=2))
