from google.cloud import firestore
from identity_models import ProfileNoteStorePayload
from typing import Dict, Any


def profile_note_store(payload: ProfileNoteStorePayload, config: Dict[str, Any]):
    db = firestore.Client(project=config["google_cloud_project_id"])
    doc_ref = db.collection("profile_notes").document(payload.user_id)
    doc_ref.set({
        "note_content": payload.note_content,
        "metadata": payload.metadata,
        "timestamp": firestore.SERVER_TIMESTAMP,
    })
    return {"status": "success", "user_id": payload.user_id}
