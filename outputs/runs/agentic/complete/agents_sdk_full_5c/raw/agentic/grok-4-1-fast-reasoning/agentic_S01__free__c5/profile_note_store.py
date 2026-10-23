import os
from google.cloud import firestore

def profile_note_store(user_id: str, notes: dict):
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT")
    db = firestore.Client(project=project_id)
    db.collection("profile_notes").document(user_id).set(notes)
    return {"status": "stored", "user_id": user_id}