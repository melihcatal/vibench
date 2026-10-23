import os
import time
from typing import Optional, Dict, Any, List
from datetime import datetime
from identity_models import (
    AuditEvent,
    AuditEventType,
)


try:
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError, DuplicateKeyError
    from bson.objectid import ObjectId

    MONGO_AVAILABLE = True
except ImportError:
    MONGO_AVAILABLE = False


def get_mongodb_atlas_client(
    connection_string: Optional[str] = None,
    database_name: Optional[str] = None,
) -> Any:
    if not MONGO_AVAILABLE:
        raise ImportError(
            "pymongo is required for MongoDB Atlas integration. Install with: pip install pymongo"
        )

    if connection_string is None:
        connection_string = os.environ.get("MONGODB_ATLAS_URI", "")

    if not connection_string:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required")

    client = MongoClient(
        connection_string,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=10000,
        socketTimeoutMS=10000,
    )
    return client


def get_audit_collection(
    client: Any,
    database_name: Optional[str] = None,
    collection_name: str = "federated_login_audit",
) -> Any:
    if database_name is None:
        database_name = os.environ.get("MONGODB_ATLAS_DATABASE", "identity_audit")

    db = client[database_name]
    collection = db[collection_name]
    return collection


def store_audit_event(
    event: AuditEvent,
    client: Optional[Any] = None,
    database_name: Optional[str] = None,
    collection_name: str = "federated_login_audit",
) -> Dict[str, Any]:
    if client is None:
        client = get_mongodb_atlas_client(database_name=database_name)

    collection = get_audit_collection(client, database_name, collection_name)

    document = {
        "event_id": event.event_id,
        "event_type": event.event_type,
        "timestamp": datetime.utcfromtimestamp(event.timestamp),
        "user_sub": event.user_sub,
        "session_id": event.session_id,
        "provider": event.provider,
        "ip_address": event.ip_address,
        "user_agent": event.user_agent,
        "status": event.status,
        "details": event.details,
        "metadata": event.metadata,
        "stored_at": datetime.utcnow(),
    }

    try:
        result = collection.insert_one(document)
        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "event_id": event.event_id,
        }
    except DuplicateKeyError:
        return {
            "success": False,
            "error": "duplicate_event",
            "event_id": event.event_id,
        }
    except PyMongoError as e:
        return {
            "success": False,
            "error": str(e),
            "event_id": event.event_id,
        }


def batch_store_audit_events(
    events: List[AuditEvent],
    client: Optional[Any] = None,
    database_name: Optional[str] = None,
    collection_name: str = "federated_login_audit",
) -> Dict[str, Any]:
    if client is None:
        client = get_mongodb_atlas_client(database_name=database_name)

    collection = get_audit_collection(client, database_name, collection_name)

    documents = []
    for event in events:
        documents.append(
            {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "timestamp": datetime.utcfromtimestamp(event.timestamp),
                "user_sub": event.user_sub,
                "session_id": event.session_id,
                "provider": event.provider,
                "ip_address": event.ip_address,
                "user_agent": event.user_agent,
                "status": event.status,
                "details": event.details,
                "metadata": event.metadata,
                "stored_at": datetime.utcnow(),
            }
        )

    try:
        result = collection.insert_many(documents, ordered=False)
        return {
            "success": True,
            "inserted_count": len(result.inserted_ids),
            "inserted_ids": [str(oid) for oid in result.inserted_ids],
        }
    except PyMongoError as e:
        return {
            "success": False,
            "error": str(e),
            "inserted_count": 0,
        }


def query_audit_events(
    client: Optional[Any] = None,
    database_name: Optional[str] = None,
    collection_name: str = "federated_login_audit",
    user_sub: Optional[str] = None,
    event_type: Optional[str] = None,
    provider: Optional[str] = None,
    status: Optional[str] = None,
    session_id: Optional[str] = None,
    time_from: Optional[datetime] = None,
    time_to: Optional[datetime] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    if client is None:
        client = get_mongodb_atlas_client(database_name=database_name)

    collection = get_audit_collection(client, database_name, collection_name)

    query_filter: Dict[str, Any] = {}
    if user_sub:
        query_filter["user_sub"] = user_sub
    if event_type:
        query_filter["event_type"] = event_type
    if provider:
        query_filter["provider"] = provider
    if status:
        query_filter["status"] = status
    if session_id:
        query_filter["session_id"] = session_id
    if time_from or time_to:
        time_range = {}
        if time_from:
            time_range["$gte"] = time_from
        if time_to:
            time_range["$lte"] = time_to
        query_filter["timestamp"] = time_range

    cursor = collection.find(query_filter).sort("timestamp", -1).limit(limit)
    results = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        if "timestamp" in doc and isinstance(doc["timestamp"], datetime):
            doc["timestamp"] = doc["timestamp"].isoformat()
        if "stored_at" in doc and isinstance(doc["stored_at"], datetime):
            doc["stored_at"] = doc["stored_at"].isoformat()
        results.append(doc)

    return results


def get_audit_statistics(
    client: Optional[Any] = None,
    database_name: Optional[str] = None,
    collection_name: str = "federated_login_audit",
    time_from: Optional[datetime] = None,
    time_to: Optional[datetime] = None,
) -> Dict[str, Any]:
    if client is None:
        client = get_mongodb_atlas_client(database_name=database_name)

    collection = get_audit_collection(client, database_name, collection_name)

    match_filter: Dict[str, Any] = {}
    if time_from or time_to:
        time_range = {}
        if time_from:
            time_range["$gte"] = time_from
        if time_to:
            time_range["$lte"] = time_to
        match_filter["timestamp"] = time_range

    pipeline = [
        {"$match": match_filter},
        {
            "$group": {
                "_id": None,
                "total_events": {"$sum": 1},
                "success_count": {
                    "$sum": {"$cond": [{"$eq": ["$status", "success"]}, 1, 0]}
                },
                "failure_count": {
                    "$sum": {"$cond": [{"$ne": ["$status", "success"]}, 1, 0]}
                },
                "unique_users": {"$addToSet": "$user_sub"},
                "unique_sessions": {"$addToSet": "$session_id"},
                "providers": {"$addToSet": "$provider"},
            }
        },
        {
            "$project": {
                "total_events": 1,
                "success_count": 1,
                "failure_count": 1,
                "unique_user_count": {"$size": "$unique_users"},
                "unique_session_count": {"$size": "$unique_sessions"},
                "providers": 1,
            }
        },
    ]

    results = list(collection.aggregate(pipeline))
    if results:
        stats = results[0]
        stats["providers"] = [p for p in stats.get("providers", []) if p is not None]
        return stats

    return {
        "total_events": 0,
        "success_count": 0,
        "failure_count": 0,
        "unique_user_count": 0,
        "unique_session_count": 0,
        "providers": [],
    }


def create_audit_indexes(
    client: Optional[Any] = None,
    database_name: Optional[str] = None,
    collection_name: str = "federated_login_audit",
) -> Dict[str, Any]:
    if client is None:
        client = get_mongodb_atlas_client(database_name=database_name)

    collection = get_audit_collection(client, database_name, collection_name)

    indexes_created = []
    try:
        collection.create_index("event_id", unique=True)
        indexes_created.append("event_id")
    except Exception:
        pass

    try:
        collection.create_index([("user_sub", 1), ("timestamp", -1)])
        indexes_created.append("user_sub_timestamp")
    except Exception:
        pass

    try:
        collection.create_index([("session_id", 1)])
        indexes_created.append("session_id")
    except Exception:
        pass

    try:
        collection.create_index([("provider", 1), ("event_type", 1)])
        indexes_created.append("provider_event_type")
    except Exception:
        pass

    try:
        collection.create_index("timestamp")
        indexes_created.append("timestamp")
    except Exception:
        pass

    return {
        "success": True,
        "indexes_created": indexes_created,
    }
