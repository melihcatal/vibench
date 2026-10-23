"""
login_audit_store.py - Persist federated-login audit records in a
managed document store.

Provider: MongoDB Atlas
SDK: pymongo
Auth env vars: MONGODB_ATLAS_URI
"""

import os
from datetime import datetime, timezone
from typing import Any, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


def get_mongo_client() -> MongoClient:
    """
    Create a MongoDB Atlas client using the MONGODB_ATLAS_URI
    environment variable.
    """
    uri = os.environ.get("MONGODB_ATLAS_URI", "")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable must be set")
    return MongoClient(uri)


def get_audit_database(client: MongoClient, db_name: str = "identity_audit") -> Database:
    """Get or create the audit database in MongoDB Atlas."""
    return client[db_name]


def get_audit_collection(db: Database, collection_name: str = "login_events") -> Collection:
    """Get the audit events collection."""
    return db[collection_name]


def store_audit_event(
    event: dict,
    collection: Optional[Collection] = None,
) -> str:
    """
    Store a single federated-login audit event in MongoDB Atlas.

    Adds timestamps and returns the inserted document ID.
    """
    if collection is None:
        client = get_mongo_client()
        db = get_audit_database(client)
        collection = get_audit_collection(db)

    document = {
        **event,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    result = collection.insert_one(document)
    return str(result.inserted_id)


def store_audit_events(
    events: list[dict],
    collection: Optional[Collection] = None,
) -> list[str]:
    """
    Bulk store multiple federated-login audit events in MongoDB Atlas.

    Returns a list of inserted document IDs.
    """
    if collection is None:
        client = get_mongo_client()
        db = get_audit_database(client)
        collection = get_audit_collection(db)

    now = datetime.now(timezone.utc)
    documents = [
        {
            **event,
            "created_at": now,
            "updated_at": now,
        }
        for event in events
    ]

    result = collection.insert_many(documents)
    return [str(oid) for oid in result.inserted_ids]


def query_audit_events(
    user_id: Optional[str] = None,
    provider: Optional[str] = None,
    event_type: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 100,
    collection: Optional[Collection] = None,
) -> list[dict]:
    """
    Query federated-login audit events from MongoDB Atlas.

    Supports filtering by user, provider, event type, and time range.
    """
    if collection is None:
        client = get_mongo_client()
        db = get_audit_database(client)
        collection = get_audit_collection(db)

    query: dict[str, Any] = {}

    if user_id:
        query["user_id"] = user_id
    if provider:
        query["provider"] = provider
    if event_type:
        query["event_type"] = event_type

    time_filter: dict = {}
    if start_time:
        time_filter["$gte"] = start_time
    if end_time:
        time_filter["$lte"] = end_time
    if time_filter:
        query["created_at"] = time_filter

    cursor = collection.find(query).sort("created_at", -1).limit(limit)
    return list(cursor)


def get_audit_summary(
    collection: Optional[Collection] = None,
    days: int = 30,
) -> dict:
    """
    Generate a summary of audit events from MongoDB Atlas for the
    specified number of days.

    Returns event counts by type, provider, and error status.
    """
    if collection is None:
        client = get_mongo_client()
        db = get_audit_database(client)
        collection = get_audit_collection(db)

    cutoff = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    cutoff = cutoff.replace(day=cutoff.day - days)

    pipeline = [
        {"$match": {"created_at": {"$gte": cutoff}}},
        {
            "$group": {
                "_id": {
                    "event_type": "$event_type",
                    "provider": "$provider",
                },
                "count": {"$sum": 1},
                "error_count": {
                    "$sum": {"$cond": [{"$ifNull": ["$error_message", False]}, 1, 0]}
                },
                "unique_users": {"$addToSet": "$user_id"},
            }
        },
    ]

    results = list(collection.aggregate(pipeline))

    summary = {
        "period_days": days,
        "start_date": cutoff.isoformat(),
        "groups": [],
    }

    for group in results:
        summary["groups"].append({
            "event_type": group["_id"]["event_type"],
            "provider": group["_id"]["provider"],
            "count": group["count"],
            "error_count": group["error_count"],
            "unique_user_count": len(group.get("unique_users", [])),
        })

    return summary


def create_audit_indexes(collection: Optional[Collection] = None) -> list[str]:
    """
    Create recommended indexes on the audit events collection
    for efficient querying in MongoDB Atlas.

    Returns a list of created index names.
    """
    if collection is None:
        client = get_mongo_client()
        db = get_audit_database(client)
        collection = get_audit_collection(db)

    indexes = [
        ([("user_id", 1), ("created_at", -1)], "idx_user_timeline"),
        ([("provider", 1), ("event_type", 1)], "idx_provider_event"),
        ([("created_at", -1)], "idx_created_at"),
        ([("state", 1)], "idx_state"),
    ]

    created = []
    for keys, name in indexes:
        try:
            collection.create_index(keys, name=name)
            created.append(name)
        except Exception:
            pass  # Index may already exist

    return created
