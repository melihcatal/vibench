"""
[LATER-STEP] Persist processed message records to MongoDB Atlas for later lookup.
Provider: MongoDB Atlas
SDK: pymongo
Auth: MONGODB_ATLAS_URI
"""

import os
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from messaging_models import PubSubEvent, ConsumeResult


def get_mongo_client():
    """
    Create and return a MongoDB Atlas client.
    Uses MONGODB_ATLAS_URI environment variable for auth.
    """
    import pymongo
    uri = os.environ.get("MONGODB_ATLAS_URI", "")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required")
    return pymongo.MongoClient(uri)


def store_message_record(
    event: PubSubEvent,
    message_id: str = "",
    processing_status: str = "received",
    collection_name: str = "message_records",
    database_name: str = None,
) -> str:
    """
    Store a processed message record in MongoDB Atlas.

    Args:
        event: The PubSubEvent to persist.
        message_id: The Pub/Sub message ID.
        processing_status: Current processing status.
        collection_name: MongoDB collection name.
        database_name: MongoDB database name (from env if not provided).

    Returns:
        The inserted document ID.
    """
    database_name = database_name or os.environ.get("MONGODB_DATABASE", "messaging_db")

    client = get_mongo_client()
    db = client[database_name]
    collection = db[collection_name]

    record = {
        "event_id": event.event_id,
        "message_id": message_id,
        "event_type": event.event_type,
        "source": event.source,
        "payload": event.payload,
        "attributes": event.attributes,
        "processing_status": processing_status,
        "timestamp": event.timestamp,
        "stored_at": datetime.now(timezone.utc).isoformat(),
    }

    result = collection.insert_one(record)
    return str(result.inserted_id)


def store_consume_result(
    consume_result: ConsumeResult,
    processing_status: str = "consumed",
    collection_name: str = "message_records",
    database_name: str = None,
) -> str:
    """
    Store a consume result as a MongoDB record.

    Args:
        consume_result: The ConsumeResult to persist.
        processing_status: Current processing status.
        collection_name: MongoDB collection name.
        database_name: MongoDB database name.

    Returns:
        The inserted document ID.
    """
    if consume_result.event is None:
        raise ValueError("ConsumeResult has no event to store")

    return store_message_record(
        event=consume_result.event,
        message_id=consume_result.message_id,
        processing_status=processing_status,
        collection_name=collection_name,
        database_name=database_name,
    )


def lookup_message_records(
    event_id: Optional[str] = None,
    event_type: Optional[str] = None,
    processing_status: Optional[str] = None,
    limit: int = 50,
    collection_name: str = "message_records",
    database_name: str = None,
) -> List[Dict[str, Any]]:
    """
    Look up stored message records by various filters.

    Args:
        event_id: Filter by event_id.
        event_type: Filter by event_type.
        processing_status: Filter by processing_status.
        limit: Maximum number of records to return.
        collection_name: MongoDB collection name.
        database_name: MongoDB database name.

    Returns:
        List of matching records as dictionaries.
    """
    database_name = database_name or os.environ.get("MONGODB_DATABASE", "messaging_db")

    client = get_mongo_client()
    db = client[database_name]
    collection = db[collection_name]

    query = {}
    if event_id:
        query["event_id"] = event_id
    if event_type:
        query["event_type"] = event_type
    if processing_status:
        query["processing_status"] = processing_status

    cursor = collection.find(query).limit(limit).sort("stored_at", -1)
    records = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        records.append(doc)

    return records
