import os

from google.cloud import firestore


def profile_note_store(user_id: str, note: str, metadata: dict) -> dict:
    db = firestore.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    doc_ref = db.collection("onboarding_notes").document(user_id)
    payload = {"user_id": user_id, "note": note, "metadata": metadata}
    doc_ref.set(payload, merge=True)
    return payload
