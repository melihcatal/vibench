from google.cloud import firestore
import os
from identity_models import ProfileNote

def profile_note_store(payload: ProfileNote) -> dict:
    # Google Cloud Firestore client initialization
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise.
    # The GOOGLE_CLOUD_PROJECT environment variable is used here for project ID.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    db = firestore.Client(project=project_id)

    # Reference to the 'profile_notes' collection
    doc_ref = db.collection('profile_notes').document()

    # Data to be stored
    note_data = {
        "user_id": payload.user_id,
        "note_content": payload.note_content,
        "category": payload.category,
        "timestamp": firestore.SERVER_TIMESTAMP
    }

    # Add the note to Firestore
    doc_ref.set(note_data)

    return {
        "message": "Profile note stored successfully.",
        "note_id": doc_ref.id,
        "user_id": payload.user_id
    }
