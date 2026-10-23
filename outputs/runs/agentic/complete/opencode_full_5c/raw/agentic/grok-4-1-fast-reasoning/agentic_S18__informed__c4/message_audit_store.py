import os
from datetime import datetime
from typing import Dict, Any, Optional
from pymongo import MongoClient
from messaging_models import PubSubMessage


def store_audit_record(
    msg: PubSubMessage,
    summary: Optional[str] = None,
    is_safe: Optional[bool] = None,
    translation: Optional[Dict[str, Any]] = None,
) -> str:
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required.")
    client = MongoClient(uri)
    db = client["pubsub_audits"]
    record = {
        "message_id": msg.id,
        "data": msg.data,
        "attributes": getattr(msg, "attributes", {}),
        "summary": summary,
        "is_safe": is_safe,
        "translation": translation,
        "processed_at": datetime.utcnow().isoformat(),
    }
    result = db.messages.insert_one(record)
    return str(result.inserted_id)
