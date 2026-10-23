"""
Persist processed message records to MongoDB Atlas for later lookup.

Uses the pymongo SDK to store and retrieve message audit records
in a MongoDB Atlas managed NoSQL document store.
Requires MONGODB_ATLAS_URI environment variable for authentication.
"""

import os
import json
from datetime import datetime, timezone
from typing import Optional, Sequence

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError


class AuditRecord:
    """Represents a processed message audit record."""

    def __init__(
        self,
        message_id: str,
        event_type: str,
        status: str,
        payload: dict,
        processed_at: Optional[str] = None,
    ):
        self.message_id = message_id
        self.event_type = event_type
        self.status = status
        self.payload = payload
        self.processed_at = processed_at or datetime.now(timezone.utc).isoformat()
        self.metadata: dict = {}

    def to_document(self) -> dict:
        return {
            "message_id": self.message_id,
            "event_type": self.event_type,
            "status": self.status,
            "payload": self.payload,
            "processed_at": self.processed_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_document(cls, doc: dict) -> "AuditRecord":
        record = cls(
            message_id=doc["message_id"],
            event_type=doc["event_type"],
            status=doc["status"],
            payload=doc.get("payload", {}),
            processed_at=doc.get("processed_at"),
        )
        record.metadata = doc.get("metadata", {})
        return record


def get_audit_collection(
    uri: Optional[str] = None,
    database: str = "messaging_audit",
    collection_name: str = "processed_messages",
) -> Collection:
    """
    Get a MongoDB Atlas collection for audit records.

    Args:
        uri: MongoDB Atlas connection URI.
        database: Database name.
        collection_name: Collection name.

    Returns:
        pymongo Collection for audit records.
    """
    conn_uri = uri or os.environ.get("MONGODB_ATLAS_URI", "")
    if not conn_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set")

    client = MongoClient(conn_uri)
    db = client[database]
    return db[collection_name]


def store_audit_record(
    record: AuditRecord,
    uri: Optional[str] = None,
    database: str = "messaging_audit",
    collection_name: str = "processed_messages",
) -> str:
    """
    Store a processed message audit record in MongoDB Atlas.

    Args:
        record: The AuditRecord to store.
        uri: MongoDB Atlas connection URI.
        database: Database name.
        collection_name: Collection name.

    Returns:
        The inserted document ID.
    """
    collection = get_audit_collection(uri, database, collection_name)
    doc = record.to_document()
    result = collection.insert_one(doc)
    return str(result.inserted_id)


def lookup_audit_record(
    message_id: str,
    uri: Optional[str] = None,
    database: str = "messaging_audit",
    collection_name: str = "processed_messages",
) -> Optional[AuditRecord]:
    """
    Look up an audit record by message ID from MongoDB Atlas.

    Args:
        message_id: The message ID to look up.
        uri: MongoDB Atlas connection URI.
        database: Database name.
        collection_name: Collection name.

    Returns:
        AuditRecord if found, None otherwise.
    """
    collection = get_audit_collection(uri, database, collection_name)
    doc = collection.find_one({"message_id": message_id})
    if doc:
        return AuditRecord.from_document(doc)
    return None


def query_audit_records(
    event_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 100,
    uri: Optional[str] = None,
    database: str = "messaging_audit",
    collection_name: str = "processed_messages",
) -> Sequence[AuditRecord]:
    """
    Query audit records from MongoDB Atlas with optional filters.

    Args:
        event_type: Filter by event type.
        status: Filter by processing status.
        limit: Maximum number of records to return.
        uri: MongoDB Atlas connection URI.
        database: Database name.
        collection_name: Collection name.

    Returns:
        Sequence of matching AuditRecords.
    """
    collection = get_audit_collection(uri, database, collection_name)

    query = {}
    if event_type:
        query["event_type"] = event_type
    if status:
        query["status"] = status

    cursor = collection.find(query).sort("processed_at", -1).limit(limit)
    return [AuditRecord.from_document(doc) for doc in cursor]


def update_audit_status(
    message_id: str,
    new_status: str,
    metadata: Optional[dict] = None,
    uri: Optional[str] = None,
    database: str = "messaging_audit",
    collection_name: str = "processed_messages",
) -> bool:
    """
    Update the status of an existing audit record in MongoDB Atlas.

    Args:
        message_id: The message ID to update.
        new_status: New processing status.
        metadata: Additional metadata to merge.
        uri: MongoDB Atlas connection URI.
        database: Database name.
        collection_name: Collection name.

    Returns:
        True if record was updated, False if not found.
    """
    collection = get_audit_collection(uri, database, collection_name)

    update_doc = {"$set": {"status": new_status}}
    if metadata:
        update_doc["$set"]["metadata"] = metadata

    result = collection.update_one({"message_id": message_id}, update_doc)
    return result.modified_count > 0


if __name__ == "__main__":
    sample_record = AuditRecord(
        message_id="msg_abc123",
        event_type="order.create",
        status="processed",
        payload={"order_id": "ord_999", "amount": 49.99},
    )
    record_id = store_audit_record(sample_record)
    print(f"Stored audit record with ID: {record_id}")
