from google.cloud import firestore
import os

from identity_client import GoogleCloudConfig
from identity_models import (
    StoreProfileNoteRequest,
    StoreProfileNoteResponse,
    ProfileNote,
)


def profile_note_store(request: StoreProfileNoteRequest) -> StoreProfileNoteResponse:
    """
    Persists onboarding notes and support metadata in Google Cloud Firestore.
    """
    if not GoogleCloudConfig.PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    # Firestore client will automatically pick up credentials from GOOGLE_APPLICATION_CREDENTIALS
    db = firestore.Client(project=GoogleCloudConfig.PROJECT_ID)

    notes_collection = db.collection("profile_notes")

    note_data = {
        "user_id": request.note.user_id,
        "note_content": request.note.note_content,
        "timestamp": request.note.timestamp,
        "metadata": request.note.metadata,
    }

    try:
        # Add a new document to the collection, Firestore will auto-generate an ID
        doc_ref = notes_collection.add(note_data)

        return StoreProfileNoteResponse(
            note_id=doc_ref[1].id  # doc_ref is (timestamp, DocumentReference)
        )
    except Exception as e:
        raise ValueError(f"Failed to store profile note: {e}")
