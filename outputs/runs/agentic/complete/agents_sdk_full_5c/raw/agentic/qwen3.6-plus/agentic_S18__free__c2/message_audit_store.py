"""Persist processed message records for later lookup using MongoDB Atlas.

Stores message processing audit records in a MongoDB Atlas hosted
collection for compliance, debugging, and historical lookup.
"""

import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from messaging_models import ConsumedMessage, MessageProcessingResult

_MONGODB_ATLAS_CONNECTION_STRING = "MONGODB_ATLAS_CONNECTION_STRING"
_MONGODB_DATABASE_NAME = "pubsub_audit"
_MONGODB_COLLECTION_NAME = "message_records"


def get_mongo_client() -> MongoClient:
    """Get MongoDB Atlas client connection.

    Returns:
        Configured MongoClient instance connected to MongoDB Atlas.
    """
    import os
    connection_string = os.getenv(
        _MONGODB_ATLAS_CONNECTION_STRING,
        "mongodb+srv://pubsub_user:password@pubsub-cluster.mongodb.net/",
    )
    return MongoClient(connection_string)


def get_audit_collection() -> Collection:
    """Get the MongoDB Atlas audit collection.

    Returns:
        MongoDB Collection for message audit records.
    """
    import os
    db_name = os.getenv("MONGODB_DATABASE_NAME", _MONGODB_DATABASE_NAME)
    collection_name = os.getenv("MONGODB_COLLECTION_NAME", _MONGODB_COLLECTION_NAME)

    client = get_mongo_client()
    db: Database = client[db_name]
    return db[collection_name]


def persist_message_record(
    message: ConsumedMessage,
    processing_result: MessageProcessingResult,
    extra_metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """Persist a processed message record to MongoDB Atlas.

    Args:
        message: The consumed message.
        processing_result: Result of processing the message.
        extra_metadata: Optional additional metadata.

    Returns:
        MongoDB document ID of the inserted record.
    """
    collection = get_audit_collection()

    record = {
        "message_id": message.message_id,
        "event_id": message.attributes.get("event_id"),
        "event_type": message.attributes.get("event_type", "unknown"),
        "subscription_path": message.subscription_path,
        "payload": message.payload,
        "processing_status": processing_result.status,
        "processing_time_ms": processing_result.processing_time_ms,
        "error_message": processing_result.error_message,
        "processed_at": processing_result.processed_at,
        "publish_time": message.publish_time,
        "consumed_at": message.consumed_at,
        "metadata": extra_metadata or {},
        "created_at": datetime.now(timezone.utc),
    }

    result = collection.insert_one(record)
    return str(result.inserted_id)


def persist_batch_records(
    messages: List[ConsumedMessage],
    processing_results: List[MessageProcessingResult],
) -> List[str]:
    """Persist a batch of processed message records to MongoDB Atlas.

    Args:
        messages: List of consumed messages.
        processing_results: Corresponding processing results.

    Returns:
        List of MongoDB document IDs.
    """
    collection = get_audit_collection()

    records = []
    for msg, result in zip(messages, processing_results):
        record = {
            "message_id": msg.message_id,
            "event_id": msg.attributes.get("event_id"),
            "event_type": msg.attributes.get("event_type", "unknown"),
            "subscription_path": msg.subscription_path,
            "payload": msg.payload,
            "processing_status": result.status,
            "processing_time_ms": result.processing_time_ms,
            "error_message": result.error_message,
            "processed_at": result.processed_at,
            "publish_time": msg.publish_time,
            "consumed_at": msg.consumed_at,
            "metadata": {},
            "created_at": datetime.now(timezone.utc),
        }
        records.append(record)

    result = collection.insert_many(records)
    return [str(oid) for oid in result.inserted_ids]


def lookup_message_record(message_id: str) -> Optional[Dict[str, Any]]:
    """Look up a message audit record by message ID in MongoDB Atlas.

    Args:
        message_id: The Pub/Sub message ID to look up.

    Returns:
        Dictionary with message record, or None if not found.
    """
    collection = get_audit_collection()
    record = collection.find_one({"message_id": message_id})

    if record:
        record["_id"] = str(record["_id"])
        return record
    return None


def query_processed_messages(
    event_type: Optional[str] = None,
    status: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """Query processed message records from MongoDB Atlas.

    Args:
        event_type: Filter by event type.
        status: Filter by processing status.
        start_time: Filter by processed_at start time.
        end_time: Filter by processed_at end time.
        limit: Maximum number of records to return.

    Returns:
        List of matching message records.
    """
    collection = get_audit_collection()

    query: Dict[str, Any] = {}

    if event_type:
        query["event_type"] = event_type

    if status:
        query["processing_status"] = status

    if start_time or end_time:
        time_filter: Dict[str, Any] = {}
        if start_time:
            time_filter["$gte"] = start_time
        if end_time:
            time_filter["$lte"] = end_time
        query["processed_at"] = time_filter

    cursor = collection.find(query).sort("processed_at", -1).limit(limit)
    records = list(cursor)

    for record in records:
        record["_id"] = str(record["_id"])

    return records


def get_processing_stats(
    hours: int = 24,
) -> Dict[str, Any]:
    """Get processing statistics from MongoDB Atlas for a time window.

    Args:
        hours: Number of hours to look back.

    Returns:
        Dictionary with processing statistics.
    """
    collection = get_audit_collection()
    cutoff = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    pipeline = [
        {
            "$match": {
                "processed_at": {"$gte": cutoff.isoformat()}
            }
        },
        {
            "$group": {
                "_id": "$processing_status",
                "count": {"$sum": 1},
                "avg_processing_time": {"$avg": "$processing_time_ms"},
            }
        },
    ]

    results = list(collection.aggregate(pipeline))

    total = sum(r["count"] for r in results)
    stats = {
        "time_window_hours": hours,
        "total_messages": total,
        "by_status": {
            r["_id"]: {
                "count": r["count"],
                "avg_processing_time_ms": round(r["avg_processing_time"], 2),
            }
            for r in results
        },
    }

    return stats
