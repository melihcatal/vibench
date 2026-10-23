import os
import json
from typing import Dict, Any, Optional
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId


def persist_message_record(message_data: Dict[str, Any]) -> Dict[str, Any]:
    """Persist processed message records for later lookup using MongoDB Atlas."""
    connection_string = os.environ.get("MONGODB_ATLAS_URI")
    if not connection_string:
        raise ValueError("MONGODB_ATLAS_URI environment variable must be set")

    try:
        client = MongoClient(connection_string)
        db = client.get_database("message_audit")
        collection = db.get_collection("processed_messages")

        audit_record = {
            "message_id": message_data.get("message_id"),
            "data": message_data.get("data", {}),
            "processing_timestamp": datetime.utcnow().isoformat(),
            "status": message_data.get("status", "processed"),
            "metadata": message_data.get("metadata", {}),
            "processing_steps": message_data.get("processing_steps", []),
            "provider": "MongoDB Atlas",
            "database": "message_audit",
            "collection": "processed_messages",
        }

        if "publish_time" in message_data:
            audit_record["original_publish_time"] = message_data["publish_time"]

        result = collection.insert_one(audit_record)

        return {
            "record_id": str(result.inserted_id),
            "message_id": audit_record["message_id"],
            "timestamp": audit_record["processing_timestamp"],
            "status": audit_record["status"],
            "provider": "MongoDB Atlas",
            "database": db.name,
            "collection": collection.name,
            "operation": "insert",
        }
    except Exception as e:
        return {
            "error": str(e),
            "provider": "MongoDB Atlas",
            "connection_env": "MONGODB_ATLAS_URI",
            "message_id": message_data.get("message_id"),
        }


def lookup_message_record(record_id: str) -> Optional[Dict[str, Any]]:
    """Look up a previously stored message record."""
    connection_string = os.environ.get("MONGODB_ATLAS_URI")
    if not connection_string:
        raise ValueError("MONGODB_ATLAS_URI environment variable must be set")

    try:
        client = MongoClient(connection_string)
        db = client.get_database("message_audit")
        collection = db.get_collection("processed_messages")

        record = collection.find_one({"_id": ObjectId(record_id)})

        if record:
            record["_id"] = str(record["_id"])
            return record

        return None
    except Exception as e:
        return {
            "error": str(e),
            "provider": "MongoDB Atlas",
            "operation": "lookup",
            "record_id": record_id,
        }
