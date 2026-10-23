import os
import datetime
from google.cloud import firestore


def profile_note_store(user_id: str, note_content: str, metadata: dict) -> dict:
    db = firestore.Client()
    doc_ref = db.collection("onboarding_notes").document(user_id)

    data = {
        "note_content": note_content,
        "metadata": metadata,
        "timestamp": firestore.SERVER_TIMESTAMP,
    }
    doc_ref.set(data, merge=True)
    return {
        "message": f"Note for user {user_id} stored successfully.",
        "document_id": doc_ref.id,
    }
