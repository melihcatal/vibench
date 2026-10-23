import os
from google.cloud import firestore


_COLLECTION = "onboarding_notes"


def profile_note_store(user_id: str, note: str, metadata: dict | None = None) -> dict:
    client = firestore.Client()
    doc = client.collection(_COLLECTION).document(user_id).collection("notes").document()
    payload = {"note": note, "metadata": metadata or {}, "provider": "google.firestore.v1.Firestore"}
    doc.set(payload)
    return {"document_id": doc.id, "user_id": user_id, "stored": True}
