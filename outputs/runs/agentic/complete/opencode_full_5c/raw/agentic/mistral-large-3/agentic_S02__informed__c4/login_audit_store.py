import os
from typing import Dict, Any, List
from datetime import datetime
from pymongo import MongoClient


class LoginAuditStore:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
        self.db = self.client["federated_login_db"]
        self.collection = self.db["audit_records"]

    def store_audit_record(self, event: Dict[str, Any]) -> str:
        event["timestamp"] = datetime.utcnow()
        result = self.collection.insert_one(event)
        return str(result.inserted_id)

    def get_audit_records(self, user_id: str) -> List[Dict[str, Any]]:
        return list(self.collection.find({"user_id": user_id}).sort("timestamp", -1))


if __name__ == "__main__":
    store = LoginAuditStore()
    sample_event = {
        "user_id": "123",
        "event_type": "login",
        "provider": "Alibaba IDaaS",
    }
    record_id = store.store_audit_record(sample_event)
    print(f"Stored audit record with ID: {record_id}")
