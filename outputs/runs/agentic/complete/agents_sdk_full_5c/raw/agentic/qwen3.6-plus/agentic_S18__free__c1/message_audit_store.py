"""message_audit_store.py - Persist processed message records using MongoDB Atlas for later lookup."""

import json
import logging
import os
from datetime import datetime, timezone
from typing import Any
import pymongo
from pymongo.errors import PyMongoError
from messaging_models import PubSubConsumeResponse

logger = logging.getLogger(__name__)

MONGODB_ATLAS_URI = os.environ.get(
    "MONGODB_ATLAS_URI",
    "mongodb+srv://admin:placeholder@cluster0.example.mongodb.net/?retryWrites=true&w=majority",
)
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "messaging_audit")
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION", "processed_messages")


_client = pymongo.MongoClient(MONGODB_ATLAS_URI)
_db = _client[MONGODB_DATABASE]
_collection = _db[MONGODB_COLLECTION]


def store_processed_message(
    message_response: PubSubConsumeResponse,
    processing_result: dict | None = None,
    metadata: dict | None = None,
) -> dict:
    """Persist a processed message record to MongoDB Atlas for audit and later lookup.

    Args:
        message_response: The consumed Pub/Sub message response.
        processing_result: Optional dictionary with processing outcome.
        metadata: Optional additional metadata for the record.

    Returns:
        Dictionary with insertion status and document ID.
    """
    now = datetime.now(timezone.utc).isoformat()

    document = {
        "message_id": message_response.message_id,
        "status": message_response.status,
        "payload": _serialize_payload(message_response.payload),
        "attributes": message_response.attributes,
        "processing_result": processing_result,
        "metadata": metadata or {},
        "stored_at": now,
        "processed_at": now,
    }

    try:
        insert_result = _collection.insert_one(document)
        document_id = str(insert_result.inserted_id)

        _collection.create_index("message_id")
        _collection.create_index("stored_at")

        logger.info(
            "Stored audit record for message_id=%s, document_id=%s in MongoDB Atlas",
            message_response.message_id,
            document_id,
        )

        return {
            "document_id": document_id,
            "message_id": message_response.message_id,
            "status": "stored",
            "stored_at": now,
        }

    except PyMongoError as exc:
        logger.error("Failed to store audit record in MongoDB Atlas: %s", exc)
        return {
            "document_id": None,
            "message_id": message_response.message_id,
            "status": "failed",
            "error": str(exc),
        }


def store_batch_processed_messages(
    message_responses: list[PubSubConsumeResponse],
) -> dict:
    """Persist a batch of processed message records to MongoDB Atlas.

    Args:
        message_responses: List of PubSubConsumeResponse objects.

    Returns:
        Dictionary with batch insertion results.
    """
    now = datetime.now(timezone.utc).isoformat()

    documents = []
    for msg in message_responses:
        documents.append(
            {
                "message_id": msg.message_id,
                "status": msg.status,
                "payload": _serialize_payload(msg.payload),
                "attributes": msg.attributes,
                "stored_at": now,
                "processed_at": now,
            }
        )

    try:
        insert_result = _collection.insert_many(documents)
        inserted_ids = [str(doc_id) for doc_id in insert_result.inserted_ids]

        logger.info(
            "Stored %d audit records in MongoDB Atlas",
            len(inserted_ids),
        )

        return {
            "document_ids": inserted_ids,
            "stored_count": len(inserted_ids),
            "status": "stored",
            "stored_at": now,
        }

    except PyMongoError as exc:
        logger.error("Failed to store batch audit records in MongoDB Atlas: %s", exc)
        return {
            "document_ids": [],
            "stored_count": 0,
            "status": "failed",
            "error": str(exc),
        }


def lookup_message_record(message_id: str) -> dict | None:
    """Look up a stored message audit record by message_id from MongoDB Atlas.

    Args:
        message_id: The original message identifier.

    Returns:
        The stored document dictionary or None if not found.
    """
    try:
        doc = _collection.find_one({"message_id": message_id})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc
    except PyMongoError as exc:
        logger.error("Failed to lookup record in MongoDB Atlas: %s", exc)
        return None


def _serialize_payload(payload: Any) -> Any:
    """Serialize payload to be JSON-safe for MongoDB storage."""
    if payload is None:
        return None
    if isinstance(payload, dict):
        return {k: _serialize_payload(v) for k, v in payload.items()}
    if isinstance(payload, (list, tuple)):
        return [_serialize_payload(item) for item in payload]
    if isinstance(payload, (datetime,)):
        return payload.isoformat()
    return payload


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_msg = PubSubConsumeResponse(
        message_id="msg_audit_001",
        payload={"event_type": "order_placed", "order_id": "ORD-777"},
        attributes={"source": "api"},
        status="consumed",
    )
    result = store_processed_message(
        sample_msg,
        processing_result={"processed": True, "duration_ms": 45},
        metadata={"worker_id": "worker-01"},
    )
    print(f"Audit store result: {result}")
