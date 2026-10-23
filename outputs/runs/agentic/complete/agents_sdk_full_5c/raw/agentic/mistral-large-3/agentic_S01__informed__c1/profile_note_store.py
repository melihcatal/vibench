import os
from typing import Dict
from google.cloud import firestore


def store_profile_note(user_id: str, note: str, metadata: Dict) -> str:
    db = firestore.Client()
    
    doc_ref = db.collection("user_onboarding_notes").document(user_id)
    doc_ref.set({
        "note": note,
        "metadata": metadata,
        "created_at": firestore.SERVER_TIMESTAMP
    })
    
    return doc_ref.id