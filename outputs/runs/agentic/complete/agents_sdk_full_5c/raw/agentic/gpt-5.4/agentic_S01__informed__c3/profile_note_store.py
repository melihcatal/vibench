from __future__ import annotations

from identity_client import MongoAtlasNoteStore, load_mongodb_atlas_config
from identity_models import ProfileNote


def profile_note_store(user_id: str, notes: str, support_metadata: dict, locale: str | None = None) -> dict:
    store = MongoAtlasNoteStore(load_mongodb_atlas_config())
    profile_note = ProfileNote(
        user_id=user_id,
        notes=notes,
        support_metadata=support_metadata,
        locale=locale,
    )
    write_result = store.upsert_profile_note(profile_note.to_document())
    return {
        "provider": "MongoDB Atlas",
        "user_id": user_id,
        "write_result": write_result,
        "document": profile_note.to_document(),
    }
