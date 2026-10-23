import os
from typing import Dict, Any
from google.cloud import firestore


def store_profile_note(user_id: str, note: str, metadata: Dict[str, Any]) -> str:
    client = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT_ID"))
    
    doc_ref = client.collection("user_onboarding_notes").document(user_id)
    doc_ref.set({
        "note": note,
        "metadata": metadata,
        "created_at": firestore.SERVER_TIMESTAMP
    })
    
    return doc_ref.id