from __future__ import annotations

import os
from datetime import datetime, timezone

from pymongo import MongoClient


def store_login_audit_record(record: dict) -> str:
    uri = os.getenv("MONGODB_ATLAS_URI", "mongodb://localhost:27017")
    client = MongoClient(uri)
    db = client[os.getenv("LOGIN_AUDIT_DB", "identity_audit")]
    collection = db[os.getenv("LOGIN_AUDIT_COLLECTION", "login_events")]
    payload = dict(record)
    payload.setdefault("created_at", datetime.now(timezone.utc).isoformat())
    result = collection.insert_one(payload)
    return str(result.inserted_id)
