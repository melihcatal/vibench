import os
import datetime
from google.cloud import firestore
from identity_models import ProfileNote

def profile_note_store(payload, config=None) -> ProfileNote:
    config = config or {}
    # Google Cloud credentials will be loaded automatically from the environment
    # if GOOGLE_APPLICATION_CREDENTIALS is set.
    # For local development, ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file.
    
    # The Google Cloud Project ID can be explicitly passed or inferred from credentials
    project_id = config.get("google_cloud_project_id", os.environ.get("GOOGLE_CLOUD_PROJECT"))
    if not project_id:
        # If not provided explicitly, firestore client can often infer from the environment.
        # However, it's good practice to ensure it's available.
        print("Warning: Google Cloud Project ID not explicitly provided. Attempting to infer.")

    db = firestore.Client(project=project_id)

    user_id = payload["user_id"]
    content = payload["content"]
    metadata = payload.get("metadata", {})

    notes_collection = db.collection("profile_notes")
    
    # Generate a unique ID for the note, or use one if provided in payload
    note_id = payload.get("note_id", notes_collection.document().id)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    note_data = {
        "user_id": user_id,
        "content": content,
        "timestamp": timestamp,
        "metadata": metadata
    }

    notes_collection.document(note_id).set(note_data)

    return ProfileNote(
        user_id=user_id,
        note_id=note_id,
        content=content,
        timestamp=timestamp,
        metadata=metadata
    )
