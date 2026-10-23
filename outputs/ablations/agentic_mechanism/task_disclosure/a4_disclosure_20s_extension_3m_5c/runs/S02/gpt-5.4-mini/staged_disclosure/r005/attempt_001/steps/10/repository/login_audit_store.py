import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from pymongo import MongoClient


class LoginAuditStore:
    def __init__(self, mongo_uri: Optional[str] = None, database_name: Optional[str] = None, collection_name: Optional[str] = None):
        self.mongo_uri = mongo_uri or os.environ["MONGODB_URI"]
        self.database_name = database_name or os.environ.get("MONGODB_DATABASE", "audit_logs")
        self.collection_name = collection_name or os.environ.get("MONGODB_COLLECTION", "login_audits")
        self.client = MongoClient(self.mongo_uri)
        self.collection = self.client[self.database_name][self.collection_name]

    def put_record(self, record: Dict[str, Any]) -> str:
        payload = dict(record)
        payload.setdefault("provider", "federated")
        payload.setdefault("created_at", datetime.now(timezone.utc))
        result = self.collection.insert_one(payload)
        return str(result.inserted_id)

    def close(self) -> None:
        self.client.close()
