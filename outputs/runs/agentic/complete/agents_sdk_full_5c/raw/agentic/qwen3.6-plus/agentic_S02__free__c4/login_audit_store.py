"""
Persist federated-login audit records in a managed document store using MongoDB Atlas.

Provider: MongoDB Atlas (https://www.mongodb.com/docs/atlas/)
"""

import os
import time
import uuid
from typing import List, Dict, Optional, Any
from datetime import datetime

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId

from identity_models import LoginAuditEvent


# MongoDB Atlas connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://user:pass@cluster0.example.mongodb.net/")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "federated_identity")
MONGODB_AUDIT_COLLECTION = os.getenv("MONGODB_AUDIT_COLLECTION", "login_audit_events")


class AuditStoreError(Exception):
    """Raised when MongoDB audit storage operation fails."""
    pass


def get_mongo_client() -> MongoClient:
    """Get MongoDB Atlas client connection."""
    return MongoClient(MONGODB_URI)


def get_audit_collection() -> Collection:
    """Get the audit events collection from MongoDB Atlas."""
    client = get_mongo_client()
    db = client[MONGODB_DB_NAME]
    return db[MONGODB_AUDIT_COLLECTION]


def ensure_indexes(collection: Optional[Collection] = None) -> None:
    """
    Create indexes on MongoDB Atlas collection for efficient audit queries.

    Indexes support common query patterns: by session, user, provider, and timestamp.
    """
    if collection is None:
        collection = get_audit_collection()

    collection.create_index([("session_id", ASCENDING)])
    collection.create_index([("user_id", ASCENDING)])
    collection.create_index([("email", ASCENDING)])
    collection.create_index([("provider", ASCENDING)])
    collection.create_index([("timestamp", DESCENDING)])
    collection.create_index([("action", ASCENDING)])
    collection.create_index([("timestamp", DESCENDING), ("provider", ASCENDING)])


def store_audit_event(event: LoginAuditEvent) -> str:
    """
    Store a single federated-login audit event in MongoDB Atlas.

    Returns the MongoDB document ObjectId as string.
    """
    try:
        collection = get_audit_collection()

        document = {
            "event_id": event.event_id,
            "session_id": event.session_id,
            "provider": event.provider,
            "user_id": event.user_id,
            "email": event.email,
            "action": event.action,
            "timestamp": event.timestamp,
            "ip_address": event.ip_address,
            "user_agent": event.user_agent,
            "auth_flow": event.auth_flow,
            "error_message": event.error_message,
            "metadata": event.metadata,
            "created_at": datetime.utcnow(),
        }

        result = collection.insert_one(document)
        return str(result.inserted_id)

    except PyMongoError as e:
        raise AuditStoreError(f"MongoDB insert failed: {str(e)}")


def store_audit_events(events: List[LoginAuditEvent]) -> List[str]:
    """
    Store multiple federated-login audit events in MongoDB Atlas (bulk insert).

    Returns list of MongoDB document ObjectIds as strings.
    """
    try:
        collection = get_audit_collection()

        documents = []
        for event in events:
            documents.append({
                "event_id": event.event_id,
                "session_id": event.session_id,
                "provider": event.provider,
                "user_id": event.user_id,
                "email": event.email,
                "action": event.action,
                "timestamp": event.timestamp,
                "ip_address": event.ip_address,
                "user_agent": event.user_agent,
                "auth_flow": event.auth_flow,
                "error_message": event.error_message,
                "metadata": event.metadata,
                "created_at": datetime.utcnow(),
            })

        result = collection.insert_many(documents)
        return [str(oid) for oid in result.inserted_ids]

    except PyMongoError as e:
        raise AuditStoreError(f"MongoDB bulk insert failed: {str(e)}")


def query_audit_events(
    provider: Optional[str] = None,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    email: Optional[str] = None,
    action: Optional[str] = None,
    time_from: Optional[int] = None,
    time_to: Optional[int] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """
    Query federated-login audit events from MongoDB Atlas.

    Supports filtering by provider, session, user, action, and time range.
    """
    try:
        collection = get_audit_collection()

        query_filter = {}
        if provider:
            query_filter["provider"] = provider
        if session_id:
            query_filter["session_id"] = session_id
        if user_id:
            query_filter["user_id"] = user_id
        if email:
            query_filter["email"] = email
        if action:
            query_filter["action"] = action
        if time_from or time_to:
            time_filter = {}
            if time_from:
                time_filter["$gte"] = time_from
            if time_to:
                time_filter["$lte"] = time_to
            query_filter["timestamp"] = time_filter

        cursor = collection.find(query_filter).sort("timestamp", DESCENDING).limit(limit)
        return list(cursor)

    except PyMongoError as e:
        raise AuditStoreError(f"MongoDB query failed: {str(e)}")


def get_session_audit(session_id: str) -> List[Dict[str, Any]]:
    """Get all audit events for a specific login session from MongoDB Atlas."""
    return query_audit_events(session_id=session_id, limit=500)


def create_audit_event_document(
    provider: str,
    action: str,
    session_id: str = "",
    user_id: str = "",
    email: str = "",
    **kwargs,
) -> LoginAuditEvent:
    """Create a LoginAuditEvent ready for MongoDB Atlas storage."""
    return LoginAuditEvent(
        event_id=str(uuid.uuid4()),
        session_id=session_id,
        provider=provider,
        user_id=user_id,
        email=email,
        action=action,
        timestamp=int(time.time()),
        ip_address=kwargs.get("ip_address", ""),
        user_agent=kwargs.get("user_agent", ""),
        auth_flow=kwargs.get("auth_flow", ""),
        error_message=kwargs.get("error_message", ""),
        metadata=kwargs.get("metadata", {}),
    )


if __name__ == "__main__":
    import json

    # Initialize indexes
    ensure_indexes()

    # Store sample audit event
    event = create_audit_event_document(
        provider="okta",
        action="login_success",
        session_id="test-session-001",
        user_id="user-123",
        email="user@example.com",
        auth_flow="authorization_code",
    )

    doc_id = store_audit_event(event)
    print(f"Stored audit event with MongoDB ID: {doc_id}")

    # Query events
    events = query_audit_events(provider="okta", limit=10)
    print(f"Found {len(events)} audit events")
