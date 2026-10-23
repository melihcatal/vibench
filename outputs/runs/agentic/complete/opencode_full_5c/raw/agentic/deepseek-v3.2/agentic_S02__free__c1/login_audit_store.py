import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId
from identity_models import AuditEvent


def get_mongo_client():
    """Get MongoDB client connection."""
    connection_string = os.getenv("MONGODB_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("MONGODB_CONNECTION_STRING environment variable is required")

    return MongoClient(connection_string)


def store_audit_event(event: AuditEvent) -> str:
    """Store federated login audit record in MongoDB."""
    client = get_mongo_client()

    try:
        db = client.get_database(os.getenv("MONGODB_DATABASE", "federated_login"))
        collection = db.get_collection("audit_events")

        event_dict = {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "user_id": event.user_id,
            "provider": event.provider,
            "ip_address": event.ip_address,
            "user_agent": event.user_agent,
            "success": event.success,
            "error_message": event.error_message,
            "metadata": event.metadata,
            "timestamp": event.timestamp,
            "created_at": datetime.now(),
            "storage_provider": "mongodb",
        }

        result = collection.insert_one(event_dict)

        return str(result.inserted_id)

    except PyMongoError as e:
        raise Exception(f"Failed to store audit event: {str(e)}")

    finally:
        client.close()


def batch_store_audit_events(events: List[AuditEvent]) -> List[str]:
    """Batch store multiple audit events in MongoDB."""
    if not events:
        return []

    client = get_mongo_client()

    try:
        db = client.get_database(os.getenv("MONGODB_DATABASE", "federated_login"))
        collection = db.get_collection("audit_events")

        event_dicts = []
        for event in events:
            event_dict = {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "user_id": event.user_id,
                "provider": event.provider,
                "ip_address": event.ip_address,
                "user_agent": event.user_agent,
                "success": event.success,
                "error_message": event.error_message,
                "metadata": event.metadata,
                "timestamp": event.timestamp,
                "created_at": datetime.now(),
                "storage_provider": "mongodb",
            }
            event_dicts.append(event_dict)

        result = collection.insert_many(event_dicts)

        return [str(id) for id in result.inserted_ids]

    except PyMongoError as e:
        raise Exception(f"Failed to batch store audit events: {str(e)}")

    finally:
        client.close()


def get_audit_events_by_user(user_id: str, limit: int = 100) -> List[Dict[str, Any]]:
    """Get audit events for a specific user."""
    client = get_mongo_client()

    try:
        db = client.get_database(os.getenv("MONGODB_DATABASE", "federated_login"))
        collection = db.get_collection("audit_events")

        query = {"user_id": user_id}
        cursor = collection.find(query).sort("timestamp", -1).limit(limit)

        events = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            events.append(doc)

        return events

    except PyMongoError as e:
        raise Exception(f"Failed to get audit events: {str(e)}")

    finally:
        client.close()


def get_audit_events_by_provider(
    provider: str, hours: int = 24
) -> List[Dict[str, Any]]:
    """Get audit events for a specific provider within time range."""
    client = get_mongo_client()

    try:
        db = client.get_database(os.getenv("MONGODB_DATABASE", "federated_login"))
        collection = db.get_collection("audit_events")

        time_threshold = datetime.now().replace(hour=datetime.now().hour - hours)

        query = {"provider": provider, "timestamp": {"$gte": time_threshold}}

        cursor = collection.find(query).sort("timestamp", -1)

        events = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            events.append(doc)

        return events

    except PyMongoError as e:
        raise Exception(f"Failed to get audit events: {str(e)}")

    finally:
        client.close()


def search_audit_events(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    provider: Optional[str] = None,
    event_type: Optional[str] = None,
    success: Optional[bool] = None,
    limit: int = 1000,
) -> List[Dict[str, Any]]:
    """Search audit events with filters."""
    client = get_mongo_client()

    try:
        db = client.get_database(os.getenv("MONGODB_DATABASE", "federated_login"))
        collection = db.get_collection("audit_events")

        query = {}

        if start_date or end_date:
            query["timestamp"] = {}
            if start_date:
                query["timestamp"]["$gte"] = start_date
            if end_date:
                query["timestamp"]["$lte"] = end_date

        if provider:
            query["provider"] = provider

        if event_type:
            query["event_type"] = event_type

        if success is not None:
            query["success"] = success

        cursor = collection.find(query).sort("timestamp", -1).limit(limit)

        events = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            events.append(doc)

        return events

    except PyMongoError as e:
        raise Exception(f"Failed to search audit events: {str(e)}")

    finally:
        client.close()


def create_audit_indexes():
    """Create indexes for efficient audit querying."""
    client = get_mongo_client()

    try:
        db = client.get_database(os.getenv("MONGODB_DATABASE", "federated_login"))
        collection = db.get_collection("audit_events")

        indexes = [
            ("timestamp", -1),
            ("user_id", 1),
            ("provider", 1),
            ("event_type", 1),
            ("success", 1),
            [("user_id", 1), ("timestamp", -1)],
            [("provider", 1), ("timestamp", -1)],
            [("event_type", 1), ("timestamp", -1)],
        ]

        for index_spec in indexes:
            if isinstance(index_spec, tuple):
                collection.create_index([index_spec])
            else:
                collection.create_index(index_spec)

        return True

    except PyMongoError as e:
        raise Exception(f"Failed to create indexes: {str(e)}")

    finally:
        client.close()


def get_audit_statistics(hours: int = 24) -> Dict[str, Any]:
    """Get audit statistics from MongoDB."""
    client = get_mongo_client()

    try:
        db = client.get_database(os.getenv("MONGODB_DATABASE", "federated_login"))
        collection = db.get_collection("audit_events")

        time_threshold = datetime.now().replace(hour=datetime.now().hour - hours)

        pipeline = [
            {"$match": {"timestamp": {"$gte": time_threshold}}},
            {
                "$group": {
                    "_id": None,
                    "total_events": {"$sum": 1},
                    "successful_events": {
                        "$sum": {"$cond": [{"$eq": ["$success", True]}, 1, 0]}
                    },
                    "failed_events": {
                        "$sum": {"$cond": [{"$eq": ["$success", False]}, 1, 0]}
                    },
                    "unique_users": {"$addToSet": "$user_id"},
                    "providers": {"$addToSet": "$provider"},
                }
            },
            {
                "$project": {
                    "total_events": 1,
                    "successful_events": 1,
                    "failed_events": 1,
                    "unique_user_count": {"$size": "$unique_users"},
                    "provider_count": {"$size": "$providers"},
                    "success_rate": {
                        "$cond": [
                            {"$eq": ["$total_events", 0]},
                            0,
                            {"$divide": ["$successful_events", "$total_events"]},
                        ]
                    },
                }
            },
        ]

        result = list(collection.aggregate(pipeline))

        if result:
            stats = result[0]
            stats["_id"] = str(stats.get("_id", ""))
            stats["time_window_hours"] = hours
            stats["calculated_at"] = datetime.now().isoformat()
            stats["storage_provider"] = "mongodb"
            return stats
        else:
            return {
                "total_events": 0,
                "successful_events": 0,
                "failed_events": 0,
                "unique_user_count": 0,
                "provider_count": 0,
                "success_rate": 0,
                "time_window_hours": hours,
                "calculated_at": datetime.now().isoformat(),
                "storage_provider": "mongodb",
            }

    except PyMongoError as e:
        raise Exception(f"Failed to get audit statistics: {str(e)}")

    finally:
        client.close()


def cleanup_old_audit_events(days_to_keep: int = 90) -> int:
    """Clean up audit events older than specified days."""
    client = get_mongo_client()

    try:
        db = client.get_database(os.getenv("MONGODB_DATABASE", "federated_login"))
        collection = db.get_collection("audit_events")

        cutoff_date = datetime.now().replace(day=datetime.now().day - days_to_keep)

        result = collection.delete_many({"timestamp": {"$lt": cutoff_date}})

        return result.deleted_count

    except PyMongoError as e:
        raise Exception(f"Failed to cleanup old audit events: {str(e)}")

    finally:
        client.close()
