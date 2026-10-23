import os
import datetime
from google.cloud import firestore
from identity_models import ProfileNote
from identity_client import get_google_project_id

def add_profile_note(note: ProfileNote) -> dict:
    project_id = get_google_project_id()
    db = firestore.Client(project=project_id)

    collection_name = "profile_notes"
    doc_ref = db.collection(collection_name).document(note.note_id)

    note_data = {
        "user_id": note.user_id,
        "note_content": note.note_content,
        "timestamp": note.timestamp or datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "metadata": note.metadata or {}
    }

    doc_ref.set(note_data)
    return {"status": "success", "note_id": note.note_id, "firestore_collection": collection_name}
