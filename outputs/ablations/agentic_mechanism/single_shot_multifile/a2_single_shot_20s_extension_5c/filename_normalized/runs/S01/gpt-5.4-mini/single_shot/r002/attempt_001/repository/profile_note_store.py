from typing import Any, Dict

from google.cloud import firestore

FIRESTORE_COLLECTION = "onboarding_notes"


def profile_note_store(note_id: str, note: Dict[str, Any]) -> Dict[str, Any]:
    db = firestore.Client()
    doc_ref = db.collection(FIRESTORE_COLLECTION).document(note_id)
    doc_ref.set(note, merge=True)
    return {"note_id": note_id, "stored": True}
