"""
Persist processed message records for later lookup using MongoDB Atlas.

Uses the pymongo SDK to store and query processed Pub/Sub message audit
records in a MongoDB Atlas cluster. Authenticated via MONGODB_ATLAS_URI.
"""

import os
import time
import uuid
from datetime import datetime, timezone
from typing import Any
from pymongo import MongoClient
from pymongo.errors import PyMongoError


MONGODB_ATLAS_URI = os.environ.get(
    "MONGODB_ATLAS_URI",
    "mongodb+srv://default_user:default_password@cluster0.mongodb.net/?retryWrites=true&w=majority",
)
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "pubsub_audit")
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION", "message_records")


def get_mongo_client() -> MongoClient:
    """Return a MongoDB Atlas client instance using the configured connection URI."""
    return MongoClient(MONGODB_ATLAS_URI)


def store_message_record(
    event_id: str,
    event_type: str,
    payload: dict[str, Any],
    status: str = "processed",
    processing_result: dict[str, Any] | None = None,
    source: str = "",
    message_id: str = "",
) -> str:
    """
    Store a processed message record in MongoDB Atlas for audit and later lookup.

    Args:
        event_id: The unique identifier of the event.
        event_type: The type/category of the event.
        payload: The original event payload.
        status: Processing status (e.g., 'processed', 'failed', 'skipped').
        processing_result: Optional detailed processing result data.
        source: The service or system that generated the event.
        message_id: The original Pub/Sub message ID.

    Returns:
        The inserted document's MongoDB ObjectId as a string.
    """
    client = get_mongo_client()
    db = client[MONGODB_DATABASE]
    collection = db[MONGODB_COLLECTION]

    record = {
        "event_id": event_id,
        "event_type": event_type,
        "source": source,
        "message_id": message_id,
        "payload": payload,
        "status": status,
        "processing_result": processing_result or {},
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "audit_id": str(uuid.uuid4()),
    }

    result = collection.insert_one(record)
    client.close()
    return str(result.inserted_id)


def lookup_message_record(event_id: str) -> dict[str, Any] | None:
    """
    Look up a processed message record by event_id from MongoDB Atlas.

    Args:
        event_id: The unique identifier of the event to find.

    Returns:
        The matching document as a dictionary, or None if not found.
    """
    client = get_mongo_client()
    db = client[MONGODB_DATABASE]
    collection = db[MONGODB_COLLECTION]

    record = collection.find_one({"event_id": event_id})
    client.close()

    if record:
        record["_id"] = str(record["_id"])
    return record


def query_message_records(
    event_type: str | None = None,
    status: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """
    Query processed message records with optional filters.

    Args:
        event_type: Filter by event type.
        status: Filter by processing status.
        limit: Maximum number of records to return.

    Returns:
        List of matching message records.
    """
    client = get_mongo_client()
    db = client[MONGODB_DATABASE]
    collection = db[MONGODB_COLLECTION]

    query_filter: dict[str, Any] = {}
    if event_type:
        query_filter["event_type"] = event_type
    if status:
        query_filter["status"] = status

    cursor = collection.find(query_filter).sort("created_at", -1).limit(limit)
    records = list(cursor)
    client.close()

    for record in records:
        record["_id"] = str(record["_id"])

    return records


def update_message_status(event_id: str, new_status: str, result_data: dict[str, Any] | None = None) -> bool:
    """
    Update the processing status of an existing message record.

    Args:
        event_id: The event ID to update.
        new_status: The new status value.
        result_data: Optional additional processing result data to merge.

    Returns:
        True if a record was found and updated, False otherwise.
    """
    client = get_mongo_client()
    db = client[MONGODB_DATABASE]
    collection = db[MONGODB_COLLECTION]

    update_fields: dict[str, Any] = {
        "status": new_status,
        "updated_at": datetime.now(timezone.utc),
    }
    if result_data:
        update_fields["processing_result"] = result_data

    result = collection.update_one(
        {"event_id": event_id},
        {"$set": update_fields},
    )
    client.close()
    return result.modified_count > 0


if __name__ == "__main__":
    import json

    doc_id = store_message_record(
        event_id="evt_audit_001",
        event_type="user.signup",
        payload={"user_id": "u001", "email": "test@example.com"},
        status="processed",
        processing_result={"summary": "User created successfully"},
        source="audit_store_cli",
    )
    print(f"Stored record with ID: {doc_id}")

    record = lookup_message_record("evt_audit_001")
    if record:
        print(json.dumps(record, indent=2, default=str))
