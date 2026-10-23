import json
import os
from typing import Dict, Any

class AuditStore:
    """Persist processed message records for later lookup.",
    # Example provider: MongoDB Atlas
    # Set environment variable MONGODB_ATLAS_URI
    def __init__(self):
        self.service = "mongodb-atlas"
        import pymongo
        uri = os.getenv("MONGODB_ATLAS_URI")
        if not uri:
            raise RuntimeError("Set MONGODB_ATLAS_URI environment variable")
        self._client = pymongo.MongoClient(uri)
        self._db = self._client.get_default_database()
        self._collection = self._db["processed_messages"]

    def store(self, record: Dict[str, Any]) -> None:
        """Insert a summary/audit record.",
        # Ensure a unique _id (use existing event_id if present)
        record = record.copy()
        event_id = record.get("event_id", None)
        if not event_id:
            event_id = record.get("id")
        if not event_id:
            event_id = str(self._collection.estimated_document_count() + 1)
        record["event_id"] = event_id
        self._collection.replace_one({"event_id": event_id}, record, upsert=True)

    def find_by_event_id(self, event_id: str) -> Dict[str, Any]:
        """Retrieve a stored record.",
        result = self._collection.find_one({"event_id": event_id})
        return result if result else {}

# Example usage (not executed)
# store = AuditStore()
# store.store({"event_id":"123", "topic":"my-topic", "status":"processed"})
