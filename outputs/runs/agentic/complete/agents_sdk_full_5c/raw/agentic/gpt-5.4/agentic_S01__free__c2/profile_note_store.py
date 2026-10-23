from __future__ import annotations

from datetime import datetime, timezone

from google.cloud import firestore

from identity_client import get_firestore_client
from identity_models import ProfileNoteStoreRequest, StoredNote


COLLECTION_NAME = "onboarding_profile_notes"


def profile_note_store(request: ProfileNoteStoreRequest):
    client = get_firestore_client()
    doc_ref = client.collection(COLLECTION_NAME).document(request.user_id)
    payload = {
        "user_id": request.user_id,
        "email": request.email,
        "notes": request.notes,
        "metadata": request.metadata or {},
        "updated_at": datetime.now(timezone.utc),
        "provider": "google_firestore",
        "firestore_type": firestore.SERVER_TIMESTAMP,
    }
    doc_ref.set(payload, merge=True)
    return StoredNote(
        document_id=doc_ref.id,
        user_id=request.user_id,
        email=request.email,
        metadata=payload["metadata"],
    )
