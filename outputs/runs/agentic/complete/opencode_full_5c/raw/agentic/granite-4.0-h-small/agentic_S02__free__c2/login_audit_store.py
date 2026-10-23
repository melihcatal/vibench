import uuid
from datetime import datetime
import json


# Placeholder for MongoDB client usage
class LoginAuditStore:
    def __init__(self):
        # In production, replace with actual DB connection logic
        self.records = []

    def save_audit(self, event):
        record = {
            "_id": str(uuid.uuid4()),
            "event_type": event["event_type"],
            "user_id": event["user_id"],
            "timestamp": datetime.utcnow().isoformat(),
            "details": event.get("details"),
        }
        self.records.append(record)
        print(f"Saved audit record: {record}")
