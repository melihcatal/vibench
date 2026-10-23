from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from pymongo import MongoClient

from identity_models import StoredProfileNote


DEFAULT_COLLECTION = "onboarding_notes"


def profile_note_store(
    user_id: str,
    note_text: str,
    metadata: Optional[Dict[str, Any]] = None,
    status: str = "active",
) -> Dict[str, Any]:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    database_name = os.getenv("MONGODB_ATLAS_DATABASE", "account_lifecycle")
    collection = client[database_name][DEFAULT_COLLECTION]
    note_id = str(uuid.uuid4())
    document = {
        "_id": note_id,
        "user_id": user_id,
        "note_text": note_text,
        "metadata": metadata or {},
        "status": status,
        "provider": "MongoDB Atlas",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    collection.insert_one(document)
    stored = StoredProfileNote(note_id=note_id, status=status, document=document)
    return {
        "note_id": stored.note_id,
        "status": stored.status,
        "document": stored.document,
    }
