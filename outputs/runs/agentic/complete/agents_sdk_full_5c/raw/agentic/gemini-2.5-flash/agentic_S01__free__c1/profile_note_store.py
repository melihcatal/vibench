from google.cloud import firestore
import os
import datetime

def profile_note_store(user_id: str, note_content: str, metadata: dict) -> dict:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS env var is set
    # Or specify project_id explicitly
    db = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id"))

    notes_ref = db.collection('onboarding_notes')

    note_data = {
        'user_id': user_id,
        'note_content': note_content,
        'metadata': metadata,
        'timestamp': datetime.datetime.now(tz=datetime.timezone.utc)
    }

    doc_ref = notes_ref.add(note_data)

    return {"document_id": doc_ref[1].id, **note_data}
