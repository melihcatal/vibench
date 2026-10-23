import os
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.collection import Collection
from pymongo.database import Database
from identity_models import AuditEvent


def get_mongo_client(
    uri: str | None = None,
) -> MongoClient:
    if uri is None:
        uri = os.getenv("MONGODB_ATLAS_URI", "")

    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required")

    return MongoClient(uri, serverSelectionTimeoutMS=10000)


def get_audit_collection(
    client: MongoClient | None = None,
    database_name: str = "federated_identity",
    collection_name: str = "audit_events",
    uri: str | None = None,
) -> Collection:
    if client is None:
        client = get_mongo_client(uri=uri)
    db: Database = client[database_name]
    collection: Collection = db[collection_name]
    collection.create_index([("timestamp", DESCENDING)])
    collection.create_index([("user_id", ASCENDING)])
    collection.create_index([("event_type", ASCENDING)])
    collection.create_index([("provider", ASCENDING)])
    collection.create_index([("session_id", ASCENDING)])
    return collection


def persist_audit_event(
    event: AuditEvent,
    collection: Collection | None = None,
    uri: str | None = None,
) -> str:
    if collection is None:
        collection = get_audit_collection(uri=uri)

    event.federated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    document = event.to_dict()
    document["created_at"] = datetime.now(timezone.utc)
    document["updated_at"] = datetime.now(timezone.utc)

    result = collection.insert_one(document)
    return str(result.inserted_id)


def persist_audit_events(
    events: List[AuditEvent],
    collection: Collection | None = None,
    uri: str | None = None,
) -> List[str]:
    if collection is None:
        collection = get_audit_collection(uri=uri)

    documents = []
    for event in events:
        doc = event.to_dict()
        doc["created_at"] = datetime.now(timezone.utc)
        doc["updated_at"] = datetime.now(timezone.utc)
        documents.append(doc)

    result = collection.insert_many(documents)
    return [str(oid) for oid in result.inserted_ids]


def query_audit_events(
    collection: Collection | None = None,
    user_id: str | None = None,
    event_type: str | None = None,
    provider: str | None = None,
    session_id: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    limit: int = 100,
    uri: str | None = None,
) -> List[Dict[str, Any]]:
    if collection is None:
        collection = get_audit_collection(uri=uri)

    query: Dict[str, Any] = {}
    if user_id:
        query["user_id"] = user_id
    if event_type:
        query["event_type"] = event_type
    if provider:
        query["provider"] = provider
    if session_id:
        query["session_id"] = session_id
    if start_time or end_time:
        query["timestamp"] = {}
        if start_time:
            query["timestamp"]["$gte"] = start_time
        if end_time:
            query["timestamp"]["$lte"] = end_time

    cursor = collection.find(query).sort("timestamp", DESCENDING).limit(limit)
    return list(cursor)


def get_audit_statistics(
    collection: Collection | None = None,
    uri: str | None = None,
) -> Dict[str, Any]:
    if collection is None:
        collection = get_audit_collection(uri=uri)

    total = collection.count_documents({})

    by_provider = list(
        collection.aggregate(
            [
                {"$group": {"_id": "$provider", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
            ]
        )
    )

    by_event_type = list(
        collection.aggregate(
            [
                {"$group": {"_id": "$event_type", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
            ]
        )
    )

    by_status = list(
        collection.aggregate(
            [
                {"$group": {"_id": "$status", "count": {"$sum": 1}}},
            ]
        )
    )

    unique_users = collection.distinct("user_id")

    return {
        "total_events": total,
        "by_provider": by_provider,
        "by_event_type": by_event_type,
        "by_status": by_status,
        "unique_users_count": len(unique_users),
        "store": "mongodb_atlas",
    }


def update_audit_event(
    event_id: str,
    updates: Dict[str, Any],
    collection: Collection | None = None,
    uri: str | None = None,
) -> bool:
    if collection is None:
        collection = get_audit_collection(uri=uri)

    updates["updated_at"] = datetime.now(timezone.utc)

    result = collection.update_one(
        {"event_id": event_id},
        {"$set": updates},
    )
    return result.modified_count > 0


if __name__ == "__main__":
    from identity_models import AuditEvent, AuditEventType

    sample_event = AuditEvent(
        event_type=AuditEventType.LOGIN_COMPLETED.value,
        user_id="auth0|user123",
        session_id="sess-abc123",
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0",
        provider="auth0",
        connection="google-oauth2",
        details={"scope": "openid profile email"},
        risk_score=0.1,
        status="success",
    )

    try:
        doc_id = persist_audit_event(sample_event)
        print(f"Persisted audit event with MongoDB Atlas ID: {doc_id}")
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Set MONGODB_ATLAS_URI to persist audit events.")
