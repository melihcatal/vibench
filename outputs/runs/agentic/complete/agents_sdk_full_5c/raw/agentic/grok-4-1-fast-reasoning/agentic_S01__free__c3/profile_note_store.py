import os
from google.cloud import firestore
from typing import Dict, Any

def profile_note_store(user_id: str, notes: Dict[str, Any]) -> bool:
    project_id = os.getenv('GCP_PROJECT_ID')
    if not project_id:
        raise ValueError('GCP_PROJECT_ID not set')
    db = firestore.Client(project=project_id)
    db.collection('profile_notes').document(user_id).set(notes)
    return True