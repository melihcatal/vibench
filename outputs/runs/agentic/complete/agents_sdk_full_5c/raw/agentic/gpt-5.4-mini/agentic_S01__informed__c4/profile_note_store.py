from __future__ import annotations

from identity_client import get_identity_client
from identity_models import NoteStoreRequest


def profile_note_store(user_id: str, note: str, metadata: dict | None = None):
    client = get_identity_client()
    request = NoteStoreRequest(user_id=user_id, note=note, metadata=metadata or {})
    return client.store_note(request)
