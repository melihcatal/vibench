"""
login_audit_store.py - Persist federated-login audit records in a managed document store
Provider: MongoDB Atlas (mongodb.com) - pymongo driver for Atlas clusters
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.errors import PyMongoError, DuplicateKeyError
from pymongo.collection import Collection


MONGODB_ATLAS_URI_ENV = "MONGODB_ATLAS_URI"
DEFAULT_DB_NAME = "federated_login_audit"
DEFAULT_COLLECTION_NAME = "login_events"


def get_mongo_client(
    connection_string: Optional[str] = None,
) -> MongoClient:
    """
    Create a MongoDB Atlas client connection.

    Provider: MongoDB Atlas (mongodb.com)
    Connection string format: mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
    """
    uri = connection_string or os.environ.get(MONGODB_ATLAS_URI_ENV, "")
    if not uri:
        raise ValueError(
            f"{MONGODB_ATLAS_URI_ENV} environment variable is required. "
            "Format: mongodb+srv://<user>:<pass>@cluster.mongodb.net/"
        )

    client = MongoClient(
        uri,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
    )
    return client


def get_audit_collection(
    client: MongoClient,
    db_name: str = DEFAULT_DB_NAME,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> Collection:
    """Get or create the audit events collection in MongoDB Atlas."""
    db = client[db_name]
    collection = db[collection_name]

    # Ensure indexes for common query patterns
    collection.create_index("timestamp", background=True)
    collection.create_index("user_sub", background=True)
    collection.create_index("event_type", background=True)
    collection.create_index([("timestamp", -1), ("event_type", 1)], background=True)

    return collection


def persist_login_event(
    event_data: Dict[str, Any],
    client: Optional[MongoClient] = None,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> Dict[str, Any]:
    """
    Persist a single federated-login audit event to MongoDB Atlas.

    Provider: MongoDB Atlas (mongodb.com)

    event_data should contain:
    - user_sub: subject identifier
    - event_type: e.g. "login_success", "login_failure", "token_refresh"
    - idp_provider: identity provider (e.g. "auth0")
    - ip_address: client IP
    - user_agent: client user agent string
    - timestamp: ISO 8601 timestamp
    - metadata: additional context
    """
    effective_client = client or get_mongo_client()

    if "timestamp" not in event_data:
        event_data["timestamp"] = datetime.now(timezone.utc).isoformat()

    event_data["created_at"] = datetime.now(timezone.utc)
    event_data["stored_at"] = datetime.now(timezone.utc)

    collection = get_audit_collection(
        effective_client,
        collection_name=collection_name,
    )

    try:
        result = collection.insert_one(event_data)
        return {
            "success": True,
            "document_id": str(result.inserted_id),
            "collection": collection_name,
            "provider": "mongodb_atlas",
        }
    except DuplicateKeyError as exc:
        return {
            "success": False,
            "error": f"Duplicate event: {str(exc)}",
            "provider": "mongodb_atlas",
        }
    except PyMongoError as exc:
        return {
            "success": False,
            "error": f"MongoDB error: {str(exc)}",
            "provider": "mongodb_atlas",
        }


def persist_login_events(
    events: List[Dict[str, Any]],
    client: Optional[MongoClient] = None,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> Dict[str, Any]:
    """
    Batch persist multiple federated-login audit events to MongoDB Atlas.

    Provider: MongoDB Atlas
    """
    effective_client = client or get_mongo_client()

    now = datetime.now(timezone.utc)
    for event in events:
        if "timestamp" not in event:
            event["timestamp"] = now.isoformat()
        event["created_at"] = now
        event["stored_at"] = now

    collection = get_audit_collection(
        effective_client,
        collection_name=collection_name,
    )

    try:
        result = collection.insert_many(events, ordered=False)
        return {
            "success": True,
            "inserted_count": len(result.inserted_ids),
            "document_ids": [str(oid) for oid in result.inserted_ids],
            "collection": collection_name,
            "provider": "mongodb_atlas",
        }
    except PyMongoError as exc:
        return {
            "success": False,
            "error": f"MongoDB batch error: {str(exc)}",
            "provider": "mongodb_atlas",
            "attempted_count": len(events),
        }


def query_login_events(
    client: Optional[MongoClient] = None,
    user_sub: Optional[str] = None,
    event_type: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 100,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> Dict[str, Any]:
    """
    Query federated-login audit events from MongoDB Atlas.

    Provider: MongoDB Atlas
    """
    effective_client = client or get_mongo_client()
    collection = get_audit_collection(
        effective_client,
        collection_name=collection_name,
    )

    query = {}
    if user_sub:
        query["user_sub"] = user_sub
    if event_type:
        query["event_type"] = event_type
    if start_time or end_time:
        time_filter = {}
        if start_time:
            time_filter["$gte"] = start_time.isoformat()
        if end_time:
            time_filter["$lte"] = end_time.isoformat()
        query["timestamp"] = time_filter

    try:
        cursor = collection.find(query).sort("timestamp", -1).limit(limit)
        events = list(cursor)

        for event in events:
            event["_id"] = str(event["_id"])

        return {
            "success": True,
            "events": events,
            "count": len(events),
            "query": query,
            "provider": "mongodb_atlas",
        }
    except PyMongoError as exc:
        return {
            "success": False,
            "error": f"MongoDB query error: {str(exc)}",
            "provider": "mongodb_atlas",
        }
