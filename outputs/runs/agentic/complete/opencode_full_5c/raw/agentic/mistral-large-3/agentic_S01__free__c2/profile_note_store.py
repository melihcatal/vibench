from typing import Dict
from google.cloud import firestore


def profile_note_store(user_id: str, notes: Dict[str, str]) -> Dict[str, str]:
    db = firestore.Client()

    doc_ref = db.collection("user_onboarding_notes").document(user_id)
    doc_ref.set({"user_id": user_id, **notes, "updated_at": firestore.SERVER_TIMESTAMP})

    return {"status": "success", "user_id": user_id, "document_id": doc_ref.id}
