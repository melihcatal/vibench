from google.cloud import firestore
from identity_models import ProfileNote
import os


def profile_note_store(note: ProfileNote):
    # Initialize Firestore client
    # Project ID is usually picked up from GOOGLE_APPLICATION_CREDENTIALS or environment variables
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")  # Ensure this env var is set
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    db = firestore.Client(project=project_id)

    # Reference to the collection and document
    doc_ref = db.collection("profile_notes").document(note.note_id)

    # Set the document data. This will create or overwrite the document.
    doc_ref.set(
        {
            "user_id": note.user_id,
            "content": note.content,
            "timestamp": note.timestamp,  # Store timestamp as a string or datetime object
        }
    )

    return {"status": "success", "note_id": note.note_id}
