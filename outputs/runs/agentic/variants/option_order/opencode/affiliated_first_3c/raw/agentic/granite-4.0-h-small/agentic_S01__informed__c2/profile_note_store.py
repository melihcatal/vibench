import os
from google.cloud import firestore

db = firestore.Client()
COLLECTION = "onboarding_notes"


def store_profile_note(user_id: str, notes: dict):
    """Persist onboarding notes and support metadata for a user.

    The notes dict can contain arbitrary JSON‑serializable fields such as
    sentiment scores, flagged content, or external ticket IDs.
    """
    doc_ref = db.collection(COLLECTION).document(user_id)
    doc_ref.set(notes, merge=True)  # merge to keep previous fields
    return {"status": "ok", "user_id": user_id}


def retrieve_profile_note(user_id: str) -> dict:
    """Fetch persisted notes for a user.

    Returns an empty dict if no notes exist yet.
    """
    doc_ref = db.collection(COLLECTION).document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return {}
