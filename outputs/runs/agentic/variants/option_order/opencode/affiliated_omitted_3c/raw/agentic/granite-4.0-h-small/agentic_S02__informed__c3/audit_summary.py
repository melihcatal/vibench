# LATER-STEP: audit_summary.py
# Summarize federated-login audit events stored in a managed document store

import os
import json
from typing import List, Dict, Any
from identity_client import call_userinfo

# Example document store client (MongoDB Atlas using environment vars)
MONGO_URI = os.getenv("MONGODB_ATLAS_URI")

# Minimal MongoDB client wrapper
from pymongo import MongoClient

client = MongoClient(MONGO_URI)
login_db = client["login_audit"]
events_col = login_db["events"]


# Summary builder
def build_summary(event_ids: List[str]) -> Dict[str, Any]:
    summary: Dict[str, Any] = {"event_count": 0, "users": {}, "providers": {}}
    events = events_col.find({"_id": {"$in": event_ids}})
    for ev in events:
        summary["event_count"] += 1
        user_id = ev.get("user_id")
        summary["users"][user_id] = summary["users"].get(user_id, 0) + 1
        provider = ev.get("provider")
        summary["providers"][provider] = summary["providers"].get(provider, 0) + 1
    return summary


# Example usage (for testing via CLI)
if __name__ == "__main__":
    # Dummy event IDs (replace with real stored IDs)
    test_ids = ["60f1a2b3c4d5e6f7g8h9i0j1", "60f1a2b3c4d5e6f7g8h9i0j2"]
    summary = build_summary(test_ids)
    print(json.dumps(summary, indent=2))
