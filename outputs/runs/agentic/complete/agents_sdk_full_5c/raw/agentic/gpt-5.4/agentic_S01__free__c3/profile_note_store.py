from __future__ import annotations

import os
import uuid
from typing import Any, Dict

from google.cloud import firestore

from identity_models import ProfileNoteRecord, utc_now_iso


def profile_note_store(user_id: str, notes: str, support_metadata: Dict[str, Any]) -> dict:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    client = firestore.Client(project=project_id)
    note_id = str(uuid.uuid4())
    created_at = utc_now_iso()
    document = {
        "user_id": user_id,
        "notes": notes,
        "support_metadata": support_metadata,
        "created_at": created_at,
    }
    client.collection("onboarding_profile_notes").document(note_id).set(document)
    return ProfileNoteRecord(note_id=note_id, user_id=user_id, created_at=created_at, data=document).__dict__
