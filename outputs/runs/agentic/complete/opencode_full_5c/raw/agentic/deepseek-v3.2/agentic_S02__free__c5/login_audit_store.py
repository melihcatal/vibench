import os
from datetime import datetime
from typing import Dict, Any
from pymongo import MongoClient
from pymongo.errors import PyMongoError


def store_login_audit_record(audit_data: Dict[str, Any]):
    mongodb_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongodb_uri)

    db = client.get_database("auth_audit")
    collection = db.get_collection("login_events")

    audit_record = {
        "timestamp": datetime.utcnow(),
        "user_id": audit_data.get("user_id"),
        "provider": audit_data.get("provider"),
        "event_type": audit_data.get("event_type", "login"),
        "success": audit_data.get("success", True),
        "ip_address": audit_data.get("ip_address"),
        "user_agent": audit_data.get("user_agent"),
        "claims": audit_data.get("claims", {}),
        "metadata": audit_data.get("metadata", {}),
    }

    try:
        result = collection.insert_one(audit_record)
        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "database": "auth_audit",
            "collection": "login_events",
            "provider": "mongodb",
        }
    except PyMongoError as e:
        return {"success": False, "error": str(e), "provider": "mongodb"}
    finally:
        client.close()


def query_login_audit_records(query: Dict[str, Any] = None, limit: int = 100):
    mongodb_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongodb_uri)

    db = client.get_database("auth_audit")
    collection = db.get_collection("login_events")

    if query is None:
        query = {}

    try:
        cursor = collection.find(query).sort("timestamp", -1).limit(limit)
        records = list(cursor)

        for record in records:
            record["_id"] = str(record["_id"])

        return {
            "success": True,
            "count": len(records),
            "records": records,
            "provider": "mongodb",
        }
    except PyMongoError as e:
        return {"success": False, "error": str(e), "provider": "mongodb"}
    finally:
        client.close()
