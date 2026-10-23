import os
import datetime
from google.cloud import firestore

def profile_note_store(user_id: str, note_content: str, metadata: dict = None) -> dict:
    db = firestore.Client(project=os.environ.get("GCP_PROJECT_ID"))
    
    # Reference to a collection and a document
    doc_ref = db.collection("user_onboarding_notes").document(user_id)
    
    timestamp = datetime.datetime.now(datetime.timezone.utc)

    note_data = {
        "user_id": user_id,
        "note_content": note_content,
        "timestamp": timestamp,
        "metadata": metadata or {}
    }
    
    # Add the note to a subcollection for the user, or update the main document
    # For simplicity, let's add it to a 'notes' subcollection under the user's document
    doc_ref.collection("notes").add(note_data)

    return {
        "status": "Note stored successfully",
        "user_id": user_id,
        "note_content": note_content,
        "stored_at": timestamp.isoformat()
    }
