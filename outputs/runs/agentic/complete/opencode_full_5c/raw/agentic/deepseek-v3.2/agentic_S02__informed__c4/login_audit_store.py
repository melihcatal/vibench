import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pymongo import MongoClient
from pymongo.errors import PyMongoError


class LoginAuditStore:
    def __init__(self, connection_string: Optional[str] = None):
        self.connection_string = connection_string or os.environ.get(
            "MONGODB_ATLAS_URI"
        )
        if not self.connection_string:
            raise ValueError("MONGODB_ATLAS_URI environment variable is required")

        self.client = MongoClient(self.connection_string)
        self.db = self.client.get_database("federated_login_audit")
        self.collection = self.db.get_collection("login_events")

        self._ensure_indexes()

    def _ensure_indexes(self):
        self.collection.create_index([("timestamp", -1)])
        self.collection.create_index([("user_id", 1)])
        self.collection.create_index([("provider", 1)])
        self.collection.create_index([("status", 1)])
        self.collection.create_index([("ip_address", 1)])

    def store_login_event(self, event_data: Dict[str, Any]) -> str:
        event = {
            "user_id": event_data.get("user_id"),
            "provider": event_data.get("provider", "unknown"),
            "timestamp": event_data.get("timestamp", datetime.now().isoformat()),
            "status": event_data.get("status", "unknown"),
            "ip_address": event_data.get("ip_address"),
            "user_agent": event_data.get("user_agent"),
            "auth_method": event_data.get("auth_method", "oauth"),
            "scope": event_data.get("scope"),
            "claims_requested": event_data.get("claims_requested", []),
            "error": event_data.get("error"),
            "metadata": event_data.get("metadata", {}),
            "stored_at": datetime.now().isoformat(),
            "database": "mongodb_atlas",
            "collection": "login_events",
        }

        try:
            result = self.collection.insert_one(event)
            return str(result.inserted_id)
        except PyMongoError as e:
            raise Exception(f"Failed to store login event in MongoDB Atlas: {str(e)}")

    def get_user_login_history(
        self, user_id: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        try:
            cursor = (
                self.collection.find({"user_id": user_id})
                .sort("timestamp", -1)
                .limit(limit)
            )

            events = list(cursor)

            for event in events:
                event["_id"] = str(event["_id"])

            return events
        except PyMongoError as e:
            raise Exception(f"Failed to retrieve user login history: {str(e)}")

    def get_recent_logins(
        self, hours: int = 24, limit: int = 100
    ) -> List[Dict[str, Any]]:
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        cutoff_iso = datetime.fromtimestamp(cutoff_time).isoformat()

        try:
            cursor = (
                self.collection.find({"timestamp": {"$gte": cutoff_iso}})
                .sort("timestamp", -1)
                .limit(limit)
            )

            events = list(cursor)

            for event in events:
                event["_id"] = str(event["_id"])

            return events
        except PyMongoError as e:
            raise Exception(f"Failed to retrieve recent logins: {str(e)}")

    def get_provider_stats(
        self, provider: Optional[str] = None, days: int = 7
    ) -> Dict[str, Any]:
        cutoff_time = datetime.now().timestamp() - (days * 24 * 3600)
        cutoff_iso = datetime.fromtimestamp(cutoff_time).isoformat()

        match_filter = {"timestamp": {"$gte": cutoff_iso}}
        if provider:
            match_filter["provider"] = provider

        try:
            pipeline = [
                {"$match": match_filter},
                {
                    "$group": {
                        "_id": {"provider": "$provider", "status": "$status"},
                        "count": {"$sum": 1},
                    }
                },
                {
                    "$group": {
                        "_id": "$_id.provider",
                        "successes": {
                            "$sum": {
                                "$cond": [
                                    {"$eq": ["$_id.status", "success"]},
                                    "$count",
                                    0,
                                ]
                            }
                        },
                        "failures": {
                            "$sum": {
                                "$cond": [
                                    {"$eq": ["$_id.status", "failure"]},
                                    "$count",
                                    0,
                                ]
                            }
                        },
                        "total": {"$sum": "$count"},
                    }
                },
            ]

            results = list(self.collection.aggregate(pipeline))

            stats = {}
            for result in results:
                provider_name = result["_id"]
                stats[provider_name] = {
                    "successes": result["successes"],
                    "failures": result["failures"],
                    "total": result["total"],
                    "success_rate": (result["successes"] / result["total"] * 100)
                    if result["total"] > 0
                    else 0,
                }

            return {
                "period_days": days,
                "cutoff_time": cutoff_iso,
                "stats": stats,
                "database": "mongodb_atlas",
            }
        except PyMongoError as e:
            raise Exception(f"Failed to get provider statistics: {str(e)}")

    def close(self):
        self.client.close()


def create_audit_store() -> LoginAuditStore:
    return LoginAuditStore()


if __name__ == "__main__":
    store = LoginAuditStore()

    sample_event = {
        "user_id": "test_user_123",
        "provider": "auth0",
        "status": "success",
        "ip_address": "192.168.1.100",
        "auth_method": "pkce",
        "scope": "openid profile email",
    }

    event_id = store.store_login_event(sample_event)
    print(f"Stored login event with ID: {event_id}")

    stats = store.get_provider_stats(days=1)
    print(f"Provider stats: {stats}")

    store.close()
