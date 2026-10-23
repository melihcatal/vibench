import os
from typing import Dict

from google.cloud import firestore


def profile_note_store(user_id: str, note: str, metadata: Dict[str, str]) -> Dict[str, str]:
    client = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
    doc = client.collection("onboarding_notes").document(user_id)
    doc.set({"note": note, "metadata": metadata})
    return {"user_id": user_id, "status": "stored"}
