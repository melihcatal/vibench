from typing import Any, Dict

from google.cloud import firestore

from identity_client import build_identity_config


class NoteStoreError(RuntimeError):
    pass


def profile_note_store(user_id: str, note: Dict[str, Any]) -> Dict[str, Any]:
    cfg = build_identity_config()
    client = firestore.Client(project=cfg.api_key or None)
    doc = client.collection("onboarding_notes").document(user_id)
    doc.set(note, merge=True)
    return {"stored": True, "collection": "onboarding_notes", "document_id": user_id}
