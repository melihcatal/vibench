import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from identity_models import AuditEvent
import pymongo
from pymongo import MongoClient
from bson import ObjectId


class LoginAuditStore:
    """Persist federated-login audit records in MongoDB Atlas."""

    def __init__(self, collection_name: str = "login_audit"):
        self.connection_string = os.environ.get("MONGODB_ATLAS_URI")

        if not self.connection_string:
            raise ValueError("MONGODB_ATLAS_URI environment variable must be set")

        # Initialize MongoDB client
        self.client = MongoClient(self.connection_string)
        self.db = self.client.get_database("identity_audit")
        self.collection = self.db[collection_name]

        # Create indexes for efficient querying
        self._create_indexes()

    def _create_indexes(self):
        """Create necessary indexes for audit queries."""
        self.collection.create_index([("timestamp", pymongo.DESCENDING)])
        self.collection.create_index([("user_id", pymongo.ASCENDING)])
        self.collection.create_index([("provider", pymongo.ASCENDING)])
        self.collection.create_index([("event_type", pymongo.ASCENDING)])
        self.collection.create_index([("success", pymongo.ASCENDING)])
        self.collection.create_index(
            [("timestamp", pymongo.DESCENDING), ("provider", pymongo.ASCENDING)]
        )

    def store_event(self, event: AuditEvent) -> str:
        """Store a single audit event."""
        event_dict = {
            "event_id": event.event_id,
            "timestamp": event.timestamp,
            "user_id": event.user_id,
            "provider": event.provider,
            "event_type": event.event_type,
            "ip_address": event.ip_address,
            "user_agent": event.user_agent,
            "success": event.success,
            "details": event.details,
            "stored_at": datetime.now(),
        }

        result = self.collection.insert_one(event_dict)
        return str(result.inserted_id)

    def store_events(self, events: List[AuditEvent]) -> List[str]:
        """Store multiple audit events."""
        event_dicts = []
        for event in events:
            event_dict = {
                "event_id": event.event_id,
                "timestamp": event.timestamp,
                "user_id": event.user_id,
                "provider": event.provider,
                "event_type": event.event_type,
                "ip_address": event.ip_address,
                "user_agent": event.user_agent,
                "success": event.success,
                "details": event.details,
                "stored_at": datetime.now(),
            }
            event_dicts.append(event_dict)

        result = self.collection.insert_many(event_dicts)
        return [str(id) for id in result.inserted_ids]

    def get_event(self, event_id: str) -> Optional[AuditEvent]:
        """Retrieve an audit event by ID."""
        document = self.collection.find_one({"event_id": event_id})

        if not document:
            return None

        return self._document_to_event(document)

    def get_events_by_user(self, user_id: str, limit: int = 100) -> List[AuditEvent]:
        """Get audit events for a specific user."""
        cursor = (
            self.collection.find({"user_id": user_id})
            .sort("timestamp", pymongo.DESCENDING)
            .limit(limit)
        )

        return [self._document_to_event(doc) for doc in cursor]

    def get_events_by_time_range(
        self, start_time: datetime, end_time: datetime
    ) -> List[AuditEvent]:
        """Get audit events within a time range."""
        cursor = self.collection.find(
            {"timestamp": {"$gte": start_time, "$lte": end_time}}
        ).sort("timestamp", pymongo.DESCENDING)

        return [self._document_to_event(doc) for doc in cursor]

    def get_events_by_provider(
        self, provider: str, limit: int = 100
    ) -> List[AuditEvent]:
        """Get audit events for a specific identity provider."""
        cursor = (
            self.collection.find({"provider": provider})
            .sort("timestamp", pymongo.DESCENDING)
            .limit(limit)
        )

        return [self._document_to_event(doc) for doc in cursor]

    def get_failed_logins(self, hours: int = 24) -> List[AuditEvent]:
        """Get failed login events within the specified hours."""
        cutoff_time = datetime.now() - datetime.timedelta(hours=hours)

        cursor = self.collection.find(
            {
                "event_type": {"$regex": "login", "$options": "i"},
                "success": False,
                "timestamp": {"$gte": cutoff_time},
            }
        ).sort("timestamp", pymongo.DESCENDING)

        return [self._document_to_event(doc) for doc in cursor]

    def get_statistics(self, days: int = 7) -> Dict[str, Any]:
        """Get login statistics for the specified period."""
        cutoff_time = datetime.now() - datetime.timedelta(days=days)

        # Total events
        total_events = self.collection.count_documents(
            {"timestamp": {"$gte": cutoff_time}}
        )

        # Successful logins
        successful_logins = self.collection.count_documents(
            {
                "timestamp": {"$gte": cutoff_time},
                "event_type": {"$regex": "login", "$options": "i"},
                "success": True,
            }
        )

        # Failed logins
        failed_logins = self.collection.count_documents(
            {
                "timestamp": {"$gte": cutoff_time},
                "event_type": {"$regex": "login", "$options": "i"},
                "success": False,
            }
        )

        # Events by provider
        pipeline = [
            {"$match": {"timestamp": {"$gte": cutoff_time}}},
            {"$group": {"_id": "$provider", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
        ]
        provider_stats = list(self.collection.aggregate(pipeline))

        # Events by hour (for time series)
        pipeline = [
            {"$match": {"timestamp": {"$gte": cutoff_time}}},
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$timestamp"},
                        "month": {"$month": "$timestamp"},
                        "day": {"$day": "$timestamp"},
                        "hour": {"$hour": "$timestamp"},
                    },
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"_id": 1}},
        ]
        hourly_stats = list(self.collection.aggregate(pipeline))

        return {
            "total_events": total_events,
            "successful_logins": successful_logins,
            "failed_logins": failed_logins,
            "success_rate": (successful_logins / (successful_logins + failed_logins))
            * 100
            if (successful_logins + failed_logins) > 0
            else 0,
            "providers": [
                {"provider": stat["_id"], "count": stat["count"]}
                for stat in provider_stats
            ],
            "hourly_distribution": hourly_stats,
            "time_period_days": days,
        }

    def cleanup_old_events(self, days_to_keep: int = 90):
        """Remove audit events older than specified days."""
        cutoff_time = datetime.now() - datetime.timedelta(days=days_to_keep)

        result = self.collection.delete_many({"timestamp": {"$lt": cutoff_time}})

        return result.deleted_count

    def _document_to_event(self, document: Dict) -> AuditEvent:
        """Convert MongoDB document to AuditEvent."""
        return AuditEvent(
            event_id=document["event_id"],
            timestamp=document["timestamp"],
            user_id=document.get("user_id"),
            provider=document["provider"],
            event_type=document["event_type"],
            ip_address=document.get("ip_address"),
            user_agent=document.get("user_agent"),
            success=document["success"],
            details=document.get("details"),
        )

    def close(self):
        """Close the MongoDB connection."""
        self.client.close()
