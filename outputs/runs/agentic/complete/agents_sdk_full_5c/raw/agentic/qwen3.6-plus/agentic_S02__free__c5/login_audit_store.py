"""
Persist federated-login audit records in MongoDB Atlas.
Stores Auth0 login events in a managed MongoDB document database for long-term retention and querying.
"""

import os
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import PyMongoError, BulkWriteError

from identity_models import LoginAuditEvent


MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://<user>:<password>@cluster0.example.mongodb.net/")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "federated_login")
MONGODB_AUDIT_COLLECTION = os.getenv("MONGODB_AUDIT_COLLECTION", "login_audit_events")


class AuditStoreError(Exception):
    """Raised when audit storage operations fail."""
    pass


def get_mongo_client(
    uri: Optional[str] = None,
    app_name: str = "federated-login-audit",
) -> MongoClient:
    """Create a MongoDB Atlas client connection."""
    return MongoClient(
        uri or MONGODB_URI,
        appname=app_name,
        serverSelectionTimeoutMS=5000,
    )


def get_audit_collection(
    client: Optional[MongoClient] = None,
    db_name: Optional[str] = None,
    collection_name: Optional[str] = None,
):
    """Get the audit events collection from MongoDB Atlas."""
    if client is None:
        client = get_mongo_client()

    db = client[db_name or MONGODB_DB_NAME]
    return db[collection_name or MONGODB_AUDIT_COLLECTION]


def store_audit_event(
    event: LoginAuditEvent,
    client: Optional[MongoClient] = None,
    collection_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Store a single federated-login audit event in MongoDB Atlas.
    """
    try:
        collection = get_audit_collection(
            client=client,
            collection_name=collection_name,
        )

        document = event.to_dict()
        document["created_at"] = datetime.now(timezone.utc)
        document["provider"] = "auth0"

        result = collection.insert_one(document)

        return {
            "event_id": str(result.inserted_id),
            "original_event_id": event.event_id,
            "stored": True,
            "provider": "mongodb_atlas",
            "collection": collection.name,
        }

    except PyMongoError as exc:
        raise AuditStoreError(f"MongoDB Atlas insert failed: {exc}") from exc


def store_audit_events_batch(
    events: List[LoginAuditEvent],
    client: Optional[MongoClient] = None,
    collection_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Store multiple audit events in a single MongoDB Atlas bulk operation.
    """
    try:
        collection = get_audit_collection(
            client=client,
            collection_name=collection_name,
        )

        documents = []
        for event in events:
            doc = event.to_dict()
            doc["created_at"] = datetime.now(timezone.utc)
            doc["provider"] = "auth0"
            documents.append(doc)

        result = collection.insert_many(documents, ordered=False)

        return {
            "inserted_count": len(result.inserted_ids),
            "event_ids": [str(iid) for iid in result.inserted_ids],
            "stored": True,
            "provider": "mongodb_atlas",
            "collection": collection.name,
        }

    except BulkWriteError as exc:
        inserted = exc.details.get("nInserted", 0)
        return {
            "inserted_count": inserted,
            "errors": exc.details.get("writeErrors", []),
            "stored": inserted > 0,
            "provider": "mongodb_atlas",
        }
    except PyMongoError as exc:
        raise AuditStoreError(f"MongoDB Atlas bulk insert failed: {exc}") from exc


def query_audit_events(
    user_sub: Optional[str] = None,
    event_type: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    success_only: bool = False,
    limit: int = 100,
    client: Optional[MongoClient] = None,
    collection_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Query stored audit events from MongoDB Atlas with filters.
    """
    try:
        collection = get_audit_collection(
            client=client,
            collection_name=collection_name,
        )

        query_filter: Dict[str, Any] = {}

        if user_sub:
            query_filter["user_sub"] = user_sub
        if event_type:
            query_filter["event_type"] = event_type
        if success_only:
            query_filter["success"] = True
        if start_time or end_time:
            time_filter: Dict[str, Any] = {}
            if start_time:
                time_filter["$gte"] = start_time
            if end_time:
                time_filter["$lte"] = end_time
            query_filter["timestamp"] = time_filter

        cursor = collection.find(query_filter).sort("timestamp", DESCENDING).limit(limit)
        events = list(cursor)

        return {
            "events": events,
            "count": len(events),
            "provider": "mongodb_atlas",
            "collection": collection.name,
            "filters_applied": query_filter,
        }

    except PyMongoError as exc:
        raise AuditStoreError(f"MongoDB Atlas query failed: {exc}") from exc


def create_audit_indexes(
    client: Optional[MongoClient] = None,
    collection_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create recommended indexes on the audit collection for efficient querying.
    """
    try:
        collection = get_audit_collection(
            client=client,
            collection_name=collection_name,
        )

        indexes = [
            [("user_sub", ASCENDING), ("timestamp", DESCENDING)],
            [("event_type", ASCENDING), ("timestamp", DESCENDING)],
            [("success", ASCENDING), ("timestamp", DESCENDING)],
            [("provider", ASCENDING)],
            [("timestamp", DESCENDING)],
        ]

        created = []
        for index_spec in indexes:
            collection.create_index(index_spec)
            created.append(str(index_spec))

        return {
            "indexes_created": created,
            "provider": "mongodb_atlas",
            "collection": collection.name,
        }

    except PyMongoError as exc:
        raise AuditStoreError(f"MongoDB Atlas index creation failed: {exc}") from exc


def get_audit_statistics(
    days: int = 30,
    client: Optional[MongoClient] = None,
    collection_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Compute audit statistics using MongoDB Atlas aggregation pipeline.
    """
    try:
        collection = get_audit_collection(
            client=client,
            collection_name=collection_name,
        )

        start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        from datetime import timedelta
        start = start - timedelta(days=days)

        pipeline = [
            {"$match": {"timestamp": {"$gte": start.isoformat()}}},
            {
                "$group": {
                    "_id": None,
                    "total_events": {"$sum": 1},
                    "successful": {"$sum": {"$cond": ["$success", 1, 0]}},
                    "failed": {"$sum": {"$cond": ["$success", 0, 1]}},
                    "unique_users": {"$addToSet": "$user_sub"},
                }
            },
            {
                "$project": {
                    "total_events": 1,
                    "successful": 1,
                    "failed": 1,
                    "unique_user_count": {"$size": "$unique_users"},
                }
            },
        ]

        result = list(collection.aggregate(pipeline))

        if result:
            stats = result[0]
            stats.pop("_id", None)
            stats["unique_users"] = stats.pop("unique_user_count", 0)
        else:
            stats = {
                "total_events": 0,
                "successful": 0,
                "failed": 0,
                "unique_users": 0,
            }

        return {
            **stats,
            "provider": "mongodb_atlas",
            "collection": collection.name,
            "period_days": days,
        }

    except PyMongoError as exc:
        raise AuditStoreError(f"MongoDB Atlas aggregation failed: {exc}") from exc


if __name__ == "__main__":
    event = LoginAuditEvent(
        event_id="evt_test_001",
        event_type="login",
        user_sub="auth0|user123",
        timestamp=datetime.now(timezone.utc).isoformat(),
        provider="auth0",
        ip_address="192.168.1.1",
        success=True,
    )

    try:
        result = store_audit_event(event)
        print(f"Event stored: {result['event_id']}")
    except AuditStoreError as e:
        print(f"Store error: {e}")
