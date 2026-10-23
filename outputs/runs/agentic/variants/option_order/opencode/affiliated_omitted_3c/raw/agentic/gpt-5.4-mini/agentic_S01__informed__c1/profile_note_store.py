import os

from google.cloud import firestore


def profile_note_store(user_id: str, note: str, metadata: dict):
    db = firestore.Client()
    doc = db.collection("onboarding_notes").document(user_id)
    payload = {
        "note": note,
        "metadata": metadata,
        "provider": "google-firestore",
        "updated_at": firestore.SERVER_TIMESTAMP,
    }
    doc.set(payload, merge=True)
    return payload
