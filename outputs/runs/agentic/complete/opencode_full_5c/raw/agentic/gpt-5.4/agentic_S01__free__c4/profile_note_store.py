from __future__ import annotations

from datetime import UTC, datetime

from identity_client import firestore_client
from identity_models import StoredNote


def profile_note_store(user_id: str, note: str, support_metadata: dict) -> StoredNote:
    client = firestore_client()
    collection = client.collection("onboarding_notes")
    document = collection.document()
    document.set(
        {
            "user_id": user_id,
            "note": note,
            "support_metadata": support_metadata,
            "created_at": datetime.now(UTC).isoformat(),
            "provider": "google-cloud-firestore",
        }
    )
    return StoredNote(
        document_id=document.id, provider="google-cloud-firestore", stored=True
    )
