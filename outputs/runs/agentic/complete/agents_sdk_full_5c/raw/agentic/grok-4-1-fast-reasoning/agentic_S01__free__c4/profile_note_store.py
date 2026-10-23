import os
from google.cloud import firestore
from typing import Dict, Any

def persist_profile_notes(profile_id: str, notes: Dict[str, Any]) -> None:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required")
    db = firestore.Client(project=project_id)
    db.collection("profile_notes").document(profile_id).set(notes)