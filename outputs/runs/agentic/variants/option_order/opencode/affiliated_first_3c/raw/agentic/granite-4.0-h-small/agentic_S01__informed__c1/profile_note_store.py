import os
from google.cloud import firestore


def store_onboarding_notes(user_id: str, notes: list):
    """Persist onboarding notes and support metadata in Google Firestore."""
    db = firestore.Client()
    doc_ref = db.collection("users").document(user_id)
    doc_ref.set({"onboarding_notes": notes})
