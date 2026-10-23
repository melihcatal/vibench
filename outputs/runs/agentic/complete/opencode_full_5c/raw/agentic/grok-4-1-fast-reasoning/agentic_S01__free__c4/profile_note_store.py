import os
from google.cloud import firestore
from typing import Dict, Any


def get_firestore_db():
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set")
    return firestore.Client(project=project_id)


def profile_note_store(user_id: str, notes: Dict[str, Any]) -> Dict[str, Any]:
    db = get_firestore_db()
    doc_ref = db.collection("profile_notes").document(user_id)
    doc_ref.set(notes, merge=True)
    return {"status": "stored", "user_id": user_id}
