# LATER-STEP: login_audit_store.py
# Persist federated-login audit records in MongoDB Atlas (managed NoSQL store)

import os
import json
from typing import Dict, Any
from identity_client import load_config
from pymongo import MongoClient

# MongoDB Atlas connection string (env var)
MONGO_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")

# Helper to get a client
client = MongoClient(MONGO_ATLAS_URI)
login_db = client["login_audit"]
records_col = login_db["records"]


# Helper to insert an audit record
def store_audit(record: Dict[str, Any]) -> str:
    """Insert audit record and return the generated _id as string."""
    inserted_id = records_col.insert_one(record).inserted_id
    return str(inserted_id)


# Example audit record shape
AUDIT_SCHEMA = {
    "event_id": str,  # UUID v4
    "timestamp": str,  # ISO8601 (UTC)
    "user_id": str,  # Provider‑normalized user identifier
    "provider": str,  # e.g., 'auth0', 'google', 'microsoft'
    "event_type": str,  # 'login', 'logout', 'token_refresh', etc.
    "details": dict,  # Free‑form details (scopes, IP, device info, etc.)
    "status": str,  # 'success' or 'failure'
    "error": dict,  # Optional error payload
}

# Example usage (testing via CLI)
if __name__ == "__main__":
    sample_record = {
        "event_id": "c58f7b6a-3d4e-4b1a-9f2c-2123e5f6a7b8",
        "timestamp": "2025-04-22T14:30:00Z",
        "user_id": "auth0|123456",
        "provider": "auth0",
        "event_type": "login",
        "details": {
            "scopes": ["openid", "profile", "email"],
            "ip_address": "203.0.113.45",
            "user_agent": "Mozilla/5.0",
        },
        "status": "success",
        "error": {},
    }
    doc_id = store_audit(sample_record)
    print("Stored audit record with id:", doc_id)
