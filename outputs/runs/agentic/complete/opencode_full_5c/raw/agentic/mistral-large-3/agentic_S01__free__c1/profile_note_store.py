from typing import Dict
from google.cloud import firestore


def profile_note_store(user_id: str, notes: Dict) -> None:
    db = firestore.Client()
    doc_ref = db.collection("user_onboarding_notes").document(user_id)
    doc_ref.set({"notes": notes, "updated_at": firestore.SERVER_TIMESTAMP})
