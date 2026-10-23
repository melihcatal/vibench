"""
login_audit_store.py - Persist federated-login audit records in MongoDB
using the MongoDB Atlas managed document store.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from typing import Any

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.collection import Collection

from identity_client import AUTH0_DOMAIN
from identity_models import build_audit_record

logger = logging.getLogger(__name__)

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://<user>:<pass>@cluster0.mongodb.net/")
MONGODB_DB = os.getenv("MONGODB_DB", "federated_login")
MONGODB_AUDIT_COLLECTION = os.getenv("MONGODB_AUDIT_COLLECTION", "audit_logs")


class AuditStore:
    """Persist and query federated-login audit records in MongoDB Atlas."""

    def __init__(
        self,
        uri: str = MONGODB_URI,
        db_name: str = MONGODB_DB,
        collection_name: str = MONGODB_AUDIT_COLLECTION,
    ):
        self._client = MongoClient(uri)
        self._db = self._client[db_name]
        self._collection: Collection = self._db[collection_name]
        self._ensure_indexes()

    def _ensure_indexes(self) -> None:
        """Create indexes on the audit collection for efficient queries."""
        self._collection.create_index([("subject", ASCENDING)])
        self._collection.create_index([("event_type", ASCENDING)])
        self._collection.create_index([("timestamp", DESCENDING)])
        self._collection.create_index([("email", ASCENDING)])
        self._collection.create_index([("provider", ASCENDING)])
        self._collection.create_index(
            [("subject", ASCENDING), ("timestamp", DESCENDING)]
        )

    def insert_audit_record(self, record: dict[str, Any]) -> str:
        """
        Insert a single federated-login audit record into MongoDB Atlas.
        """
        doc = dict(record)
        doc["created_at"] = doc.get("timestamp") or datetime.now(timezone.utc).isoformat()
        doc["auth0_domain"] = AUTH0_DOMAIN
        result = self._collection.insert_one(doc)
        logger.info(
            "Inserted audit record into mongodb atlas: id=%s, event_type=%s, subject=%s",
            result.inserted_id,
            doc.get("event_type"),
            doc.get("subject"),
        )
        return str(result.inserted_id)

    def insert_batch(self, records: list[dict[str, Any]]) -> list[str]:
        """Insert a batch of audit records into MongoDB Atlas."""
        docs = []
        for record in records:
            doc = dict(record)
            doc["created_at"] = doc.get("timestamp") or datetime.now(timezone.utc).isoformat()
            doc["auth0_domain"] = AUTH0_DOMAIN
            docs.append(doc)
        result = self._collection.insert_many(docs)
        ids = [str(oid) for oid in result.inserted_ids]
        logger.info("Inserted %d audit records into mongodb atlas", len(ids))
        return ids

    def find_by_subject(self, subject: str, limit: int = 50) -> list[dict]:
        """Find audit records for a given user subject."""
        cursor = self._collection.find({"subject": subject}).sort(
            "timestamp", DESCENDING
        ).limit(limit)
        return list(cursor)

    def find_by_email(self, email: str, limit: int = 50) -> list[dict]:
        """Find audit records for a given email."""
        cursor = self._collection.find({"email": email}).sort(
            "timestamp", DESCENDING
        ).limit(limit)
        return list(cursor)

    def find_by_event_type(
        self,
        event_type: str,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int = 100,
    ) -> list[dict]:
        """Find audit records filtered by event type and optional time range."""
        query: dict[str, Any] = {"event_type": event_type}
        if start or end:
            ts_filter = {}
            if start:
                ts_filter["$gte"] = start.isoformat()
            if end:
                ts_filter["$lte"] = end.isoformat()
            query["timestamp"] = ts_filter

        cursor = self._collection.find(query).sort("timestamp", DESCENDING).limit(limit)
        return list(cursor)

    def count_events(self, hours: int = 24) -> dict[str, int]:
        """Count events by type within a time window from MongoDB Atlas."""
        from_ts = datetime.now(timezone.utc)
        from_ts = from_ts.replace(hour=from_ts.hour - hours)

        pipeline = [
            {"$match": {"timestamp": {"$gte": from_ts.isoformat()}}},
            {"$group": {"_id": "$event_type", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
        ]
        results = self._collection.aggregate(pipeline)
        return {doc["_id"]: doc["count"] for doc in results}

    def close(self) -> None:
        """Close the MongoDB Atlas client connection."""
        self._client.close()


def persist_login_audit(
    event_type: str,
    subject: str | None = None,
    email: str | None = None,
    connection: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
    details: str | None = None,
    metadata: dict | None = None,
    store: AuditStore | None = None,
) -> str:
    """
    Build and persist a federated-login audit record in MongoDB Atlas.
    """
    if store is None:
        store = AuditStore()

    record = build_audit_record(
        event_type=event_type,
        subject=subject,
        email=email,
        provider="auth0",
        connection=connection,
        ip_address=ip_address,
        user_agent=user_agent,
        metadata=metadata,
        details=details,
    )
    return store.insert_audit_record(record)


if __name__ == "__main__":
    sample_record = build_audit_record(
        event_type="login.success",
        subject="auth0|test123",
        email="user@example.com",
        connection="google-oauth2",
        details="PKCE login flow via Auth0",
    )
    print(json.dumps(sample_record, indent=2, default=str))
