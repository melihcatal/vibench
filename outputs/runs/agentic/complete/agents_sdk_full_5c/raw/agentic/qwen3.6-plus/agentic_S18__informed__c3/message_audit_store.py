"""
Persist processed message records for later lookup.

Provider: MongoDB Atlas
SDK: pymongo
Interface: SDK
Auth: MONGODB_ATLAS_URI
"""

import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure, OperationFailure

from messaging_models import (
    EventMessage,
    AuditRecord,
    ProcessingSummary,
    SafetyCheckResult,
    TranslationResult,
)


class MessageAuditStore:
    """
    MongoDB Atlas-based audit store for processed message records.
    """

    def __init__(
        self,
        connection_uri: Optional[str] = None,
        database_name: str = "messaging_audit",
        collection_name: str = "processed_messages",
    ):
        self.connection_uri = connection_uri or os.environ.get(
            "MONGODB_ATLAS_URI", "mongodb://localhost:27017"
        )
        self.database_name = database_name
        self.collection_name = collection_name
        self._client: Optional[MongoClient] = None
        self._db = None
        self._collection = None

    def _get_client(self) -> MongoClient:
        """Get or create the MongoDB Atlas client."""
        if self._client is None:
            self._client = MongoClient(
                self.connection_uri,
                serverSelectionTimeoutMS=10000,
            )
        return self._client

    def _get_collection(self):
        """Get the audit collection."""
        if self._collection is None:
            client = self._get_client()
            self._db = client[self.database_name]
            self._collection = self._db[self.collection_name]
        return self._collection

    def store_audit_record(
        self,
        record: AuditRecord,
        index: bool = True,
    ) -> str:
        """
        Store a single audit record in MongoDB Atlas.

        Args:
            record: The AuditRecord to store.
            index: Whether to ensure indexes exist.

        Returns:
            The inserted record ID.
        """
        try:
            collection = self._get_collection()

            if index:
                collection.create_index("message_id", background=True)
                collection.create_index("event_type", background=True)
                collection.create_index("processed_at", background=True)
                collection.create_index(
                    [("message_id", 1), ("event_type", 1)],
                    unique=False,
                    background=True,
                )

            doc = record.to_dict()
            doc["_id"] = record.record_id
            doc["stored_at"] = datetime.now(timezone.utc).isoformat()

            result = collection.insert_one(doc)
            return str(result.inserted_id)

        except ConnectionFailure as e:
            raise RuntimeError(f"MongoDB Atlas connection failed: {str(e)}")
        except OperationFailure as e:
            raise RuntimeError(f"MongoDB Atlas operation failed: {str(e)}")
        except PyMongoError as e:
            raise RuntimeError(f"MongoDB error: {str(e)}")

    def store_event_with_audit(
        self,
        event: EventMessage,
        status: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Create and store an audit record from an EventMessage.

        Args:
            event: The EventMessage that was processed.
            status: Processing status (e.g., 'processed', 'failed', 'dead_lettered').
            metadata: Optional additional metadata.

        Returns:
            The inserted record ID.
        """
        metadata = metadata or {}
        metadata["event_payload"] = event.payload

        record = AuditRecord(
            message_id=event.event_id,
            event_type=event.event_type,
            status=status,
            processed_at=event.timestamp,
            metadata=metadata,
        )
        return self.store_audit_record(record)

    def store_with_safety_result(
        self,
        event: EventMessage,
        safety_result: SafetyCheckResult,
        status: str = "processed",
    ) -> str:
        """
        Store an audit record with safety check results.

        Args:
            event: The EventMessage that was checked.
            safety_result: The SafetyCheckResult.
            status: Processing status.

        Returns:
            The inserted record ID.
        """
        metadata = {
            "safety_is_safe": safety_result.is_safe,
            "safety_scores": safety_result.scores,
            "safety_categories": safety_result.categories,
            "safety_checked_at": safety_result.checked_at,
        }
        return self.store_event_with_audit(
            event, status=status, metadata=metadata
        )

    def store_with_translation(
        self,
        event: EventMessage,
        translation_result: TranslationResult,
        status: str = "processed",
    ) -> str:
        """
        Store an audit record with translation results.

        Args:
            event: The EventMessage that was translated.
            translation_result: The TranslationResult.
            status: Processing status.

        Returns:
            The inserted record ID.
        """
        metadata = {
            "translated_text": translation_result.translated_text,
            "source_language": translation_result.source_language,
            "target_language": translation_result.target_language,
            "translated_at": translation_result.translated_at,
        }
        return self.store_event_with_audit(
            event, status=status, metadata=metadata
        )

    def lookup_by_message_id(
        self,
        message_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Look up audit records by message ID.

        Args:
            message_id: The message ID to search for.

        Returns:
            Dictionary with audit record data, or None.
        """
        try:
            collection = self._get_collection()
            record = collection.find_one({"message_id": message_id})
            if record:
                record.pop("_id", None)
                return record
            return None
        except PyMongoError:
            return None

    def lookup_by_event_type(
        self,
        event_type: str,
        limit: int = 100,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Look up audit records by event type.

        Args:
            event_type: The event type to search for.
            limit: Maximum number of records to return.
            status: Optional status filter.

        Returns:
            List of audit record dictionaries.
        """
        try:
            collection = self._get_collection()
            query: Dict[str, Any] = {"event_type": event_type}
            if status:
                query["status"] = status

            cursor = collection.find(query).sort("processed_at", -1).limit(limit)
            records = []
            for doc in cursor:
                doc.pop("_id", None)
                records.append(doc)
            return records
        except PyMongoError:
            return []

    def get_processing_summary(
        self,
        time_range_hours: int = 24,
    ) -> Dict[str, Any]:
        """
        Get a processing summary from recent audit records.

        Args:
            time_range_hours: Number of hours to look back.

        Returns:
            Dictionary with processing statistics.
        """
        try:
            collection = self._get_collection()
            cutoff = datetime.now(timezone.utc).timestamp() - (time_range_hours * 3600)

            pipeline = [
                {
                    "$match": {
                        "processed_at": {
                            "$gte": datetime.fromtimestamp(cutoff, tz=timezone.utc).isoformat()
                        }
                    }
                },
                {
                    "$group": {
                        "_id": "$status",
                        "count": {"$sum": 1},
                        "event_types": {"$addToSet": "$event_type"},
                    }
                },
            ]

            results = list(collection.aggregate(pipeline))

            summary = {"total": 0, "by_status": {}, "event_types": set()}
            for result in results:
                status = result["_id"]
                count = result["count"]
                summary["by_status"][status] = count
                summary["total"] += count
                summary["event_types"].update(result.get("event_types", []))

            summary["event_types"] = list(summary["event_types"])
            return summary

        except PyMongoError:
            return {"total": 0, "by_status": {}, "event_types": []}

    def close(self) -> None:
        """Close the MongoDB client connection."""
        if self._client is not None:
            self._client.close()
            self._client = None
            self._collection = None
            self._db = None


def store_processed_message(
    event: EventMessage,
    status: str,
    metadata: Optional[Dict[str, Any]] = None,
    store: Optional[MessageAuditStore] = None,
) -> str:
    """
    Convenience function to store a processed message audit record.

    Args:
        event: The EventMessage that was processed.
        status: Processing status.
        metadata: Optional additional metadata.
        store: Optional MessageAuditStore instance.

    Returns:
        The inserted record ID.
    """
    audit_store = store or MessageAuditStore()
    try:
        record_id = audit_store.store_event_with_audit(event, status, metadata)
        return record_id
    finally:
        if store is None:
            audit_store.close()


def store_batch_messages(
    events: List[EventMessage],
    status: str,
    store: Optional[MessageAuditStore] = None,
) -> List[str]:
    """
    Store multiple processed message audit records.

    Args:
        events: List of EventMessage objects.
        status: Processing status for all messages.
        store: Optional MessageAuditStore instance.

    Returns:
        List of inserted record IDs.
    """
    audit_store = store or MessageAuditStore()
    record_ids = []
    try:
        for event in events:
            record_id = audit_store.store_event_with_audit(event, status)
            record_ids.append(record_id)
        return record_ids
    finally:
        if store is None:
            audit_store.close()
