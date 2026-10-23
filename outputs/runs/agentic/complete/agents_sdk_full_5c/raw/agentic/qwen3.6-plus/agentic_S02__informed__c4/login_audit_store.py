"""
Persist federated-login audit records in MongoDB Atlas.

Provider: MongoDB Atlas
Environment variable: MONGODB_ATLAS_URI

Stores and queries federated-login audit events in a managed
MongoDB Atlas document store with indexed collections for
efficient retrieval of login history and audit trails.
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Optional

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import PyMongoError


class LoginAuditStore:
    """Persists and queries federated-login audit records in MongoDB Atlas."""

    DEFAULT_DATABASE = "federated_identity"
    DEFAULT_COLLECTION = "login_audit_events"

    def __init__(
        self,
        uri: Optional[str] = None,
        database: Optional[str] = None,
        collection: Optional[str] = None,
    ):
        self.uri = uri or os.environ.get("MONGODB_ATLAS_URI", "")
        if not self.uri:
            raise ValueError(
                "MongoDB Atlas URI is required. Set MONGODB_ATLAS_URI."
            )

        self.database_name = database or self.DEFAULT_DATABASE
        self.collection_name = collection or self.DEFAULT_COLLECTION

        self.client = MongoClient(self.uri)
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection_name]

        self._ensure_indexes()

    def _ensure_indexes(self):
        """Create indexes for efficient audit record queries."""
        self.collection.create_index([("user_id", ASCENDING)])
        self.collection.create_index([("timestamp", DESCENDING)])
        self.collection.create_index([("event_type", ASCENDING)])
        self.collection.create_index([("provider", ASCENDING)])
        self.collection.create_index(
            [("user_id", ASCENDING), ("timestamp", DESCENDING)]
        )

    def store_event(self, event: dict[str, Any]) -> str:
        """
        Store a single federated-login audit event in MongoDB Atlas.

        Args:
            event: Dict with event data. Should include at minimum:
                - user_id: The federated user subject
                - event_type: e.g., "login_success", "login_failure", "token_refresh"
                - provider: The identity provider (e.g., "auth0", "google-oauth2")
                - timestamp: ISO 8601 timestamp or datetime

        Returns:
            The inserted document ID.
        """
        record = self._prepare_record(event)
        result = self.collection.insert_one(record)
        return str(result.inserted_id)

    def store_events(self, events: list[dict[str, Any]]) -> list[str]:
        """
        Store multiple federated-login audit events in MongoDB Atlas.

        Returns a list of inserted document IDs.
        """
        records = [self._prepare_record(e) for e in events]
        result = self.collection.insert_many(records)
        return [str(oid) for oid in result.inserted_ids]

    def query_events(
        self,
        user_id: Optional[str] = None,
        event_type: Optional[str] = None,
        provider: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100,
        sort: str = "desc",
    ) -> list[dict[str, Any]]:
        """
        Query federated-login audit events from MongoDB Atlas.

        Args:
            user_id: Filter by federated user subject
            event_type: Filter by event type
            provider: Filter by identity provider
            start_time: Start of time range
            end_time: End of time range
            limit: Maximum number of results
            sort: "desc" or "asc" for timestamp ordering

        Returns:
            List of matching audit event dicts.
        """
        query: dict[str, Any] = {}

        if user_id:
            query["user_id"] = user_id
        if event_type:
            query["event_type"] = event_type
        if provider:
            query["provider"] = provider
        if start_time or end_time:
            query["timestamp"] = {}
            if start_time:
                query["timestamp"]["$gte"] = start_time
            if end_time:
                query["timestamp"]["$lte"] = end_time

        sort_direction = DESCENDING if sort == "desc" else ASCENDING
        cursor = self.collection.find(query).sort("timestamp", sort_direction).limit(limit)

        results = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)

        return results

    def get_user_login_history(
        self,
        user_id: str,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """
        Get the login history for a specific federated user.

        Returns the most recent login events for the user.
        """
        return self.query_events(
            user_id=user_id,
            limit=limit,
            sort="desc",
        )

    def get_provider_stats(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> list[dict[str, Any]]:
        """
        Get aggregated statistics by identity provider from MongoDB Atlas.

        Returns a list of dicts with provider, count, success_count, failure_count.
        """
        match: dict[str, Any] = {}
        if start_time or end_time:
            match["timestamp"] = {}
            if start_time:
                match["timestamp"]["$gte"] = start_time
            if end_time:
                match["timestamp"]["$lte"] = end_time

        pipeline = [
            {"$match": match},
            {
                "$group": {
                    "_id": "$provider",
                    "count": {"$sum": 1},
                    "success_count": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$event_type", "login_success"]},
                                1,
                                0,
                            ]
                        }
                    },
                    "failure_count": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$event_type", "login_failure"]},
                                1,
                                0,
                            ]
                        }
                    },
                }
            },
            {"$sort": {"count": -1}},
        ]

        results = list(self.collection.aggregate(pipeline))
        for r in results:
            r["provider"] = r.pop("_id")
        return results

    def _prepare_record(self, event: dict[str, Any]) -> dict[str, Any]:
        """Prepare an event dict for MongoDB Atlas storage."""
        record = dict(event)

        if "timestamp" not in record:
            record["timestamp"] = datetime.utcnow()
        elif isinstance(record["timestamp"], str):
            try:
                record["timestamp"] = datetime.fromisoformat(
                    record["timestamp"].replace("Z", "+00:00")
                )
            except ValueError:
                record["timestamp"] = datetime.utcnow()

        record["stored_at"] = datetime.utcnow()
        return record

    def close(self):
        """Close the MongoDB Atlas connection."""
        self.client.close()


def store_audit_event(
    event: dict[str, Any],
    uri: Optional[str] = None,
) -> str:
    """
    Convenience function to store a federated-login audit event in MongoDB Atlas.

    Returns the inserted document ID.
    """
    store = LoginAuditStore(uri=uri)
    try:
        return store.store_event(event)
    finally:
        store.close()


def query_audit_events(
    user_id: Optional[str] = None,
    event_type: Optional[str] = None,
    provider: Optional[str] = None,
    limit: int = 100,
    uri: Optional[str] = None,
) -> list[dict[str, Any]]:
    """
    Convenience function to query federated-login audit events from MongoDB Atlas.

    Returns a list of matching event dicts.
    """
    store = LoginAuditStore(uri=uri)
    try:
        return store.query_events(
            user_id=user_id,
            event_type=event_type,
            provider=provider,
            limit=limit,
        )
    finally:
        store.close()


if __name__ == "__main__":
    store = LoginAuditStore()
    event_id = store.store_event({
        "user_id": "auth0|user123",
        "event_type": "login_success",
        "provider": "google-oauth2",
        "ip": "192.168.1.1",
        "user_agent": "Mozilla/5.0",
    })
    print(f"Stored event with ID: {event_id}")

    history = store.get_user_login_history("auth0|user123")
    print(f"Found {len(history)} events for user")
    store.close()
