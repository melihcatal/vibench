from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from pymongo import MongoClient

from identity_models import ProfileNoteRecord


def profile_note_store(
    user_id: str,
    status: str,
    locale: Optional[str] = None,
    notes: Optional[str] = None,
    support_metadata: Optional[Dict[str, Any]] = None,
) -> ProfileNoteRecord:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    database = client[os.getenv("MONGODB_ATLAS_DATABASE", "account_lifecycle")]
    collection = database[os.getenv("MONGODB_ATLAS_COLLECTION", "profile_notes")]
    note_id = str(uuid.uuid4())
    document = {
        "_id": note_id,
        "user_id": user_id,
        "status": status,
        "locale": locale,
        "notes": notes,
        "support_metadata": support_metadata or {},
        "created_at": datetime.now(timezone.utc),
    }
    collection.insert_one(document)
    return ProfileNoteRecord(
        note_id=note_id,
        user_id=user_id,
        status=status,
        locale=locale,
        notes=notes,
        support_metadata=support_metadata or {},
    )
