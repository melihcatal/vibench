import os
from google.cloud import firestore
from typing import Any

def persist_profile_notes(user_id: str, notes: dict[str, Any]) -> bool:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    db = firestore.Client(project=project_id)
    db.collection("onboarding_notes").document(user_id).set(notes)
    return True