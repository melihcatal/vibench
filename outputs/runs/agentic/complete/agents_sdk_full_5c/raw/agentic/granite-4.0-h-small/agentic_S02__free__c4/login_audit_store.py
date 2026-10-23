import json
import uuid
from datetime import datetime
from pymongo import MongoClient, errors

# Later-step scored file: login_audit_store.py
# Persist federated-login audit records in MongoDB Atlas (managed document store)

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://dummy:dummy@example-cluster.mongodb.net")
DB_NAME = "federated_login"
COLLECTION_NAME = "audit"

class LoginAuditStore:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def insert_audit(self, event: dict) -> str:
        # Ensure required fields exist
        if not event.get("user_id") or not event.get("provider") or not event.get("event_type"):
            raise ValueError("Missing required audit fields")
        # Generate UUID for event_id
        event_id = str(uuid.uuid4())
        event["event_id"] = event_id
        event["timestamp"] = datetime.utcnow()
        try:
            result = self.collection.insert_one(event)
            return event_id
        except errors.PyMongoError as exc:
            raise RuntimeError(f"Failed to insert audit event: {exc}")

    def find_by_user(self, user_id: str, limit: int = 20) -> list[dict]:
        return list(self.collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit))

    def find_recent(self, limit: int = 50) -> list[dict]:
        return list(self.collection.find().sort("timestamp", -1).limit(limit))

# Example usage (CLI)
if __name__ == "__main__":
    import sys
    store = LoginAuditStore()
    sample = {
        "user_id": "u12345",
        "provider": "google",
        "event_type": "login_success",
        "details": {
            "ip": "203.0.113.10",
            "user_agent": "Mozilla/5.0"
        }
    }
    event_id = store.insert_audit(sample)
    print(f"Inserted audit event {event_id}")
