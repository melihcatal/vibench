from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from google.cloud import firestore

from identity_models import StoredProfileNote


def profile_note_store(
    user_id: str, notes: Dict[str, Any], collection: str = "onboarding_notes"
) -> StoredProfileNote:
    client = firestore.Client()
    document_id = user_id
    payload = {
        "user_id": user_id,
        "notes": notes,
        "updated_at": datetime.now(timezone.utc),
    }
    doc_ref = client.collection(collection).document(document_id)
    snapshot = doc_ref.get()
    doc_ref.set(payload, merge=True)
    return StoredProfileNote(
        document_id=document_id,
        collection=collection,
        created=not snapshot.exists,
    )
