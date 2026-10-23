import os
from google.cloud import firestore
from identity_models import ProfileNote, ProfileNoteStorePayload, ProfileNoteStoreResponse

def profile_note_store(payload: ProfileNoteStorePayload) -> ProfileNoteStoreResponse:
    # Initialize Firestore client
    # Google Cloud credentials are typically handled by GOOGLE_APPLICATION_CREDENTIALS environment variable
    # or by running in a Google Cloud environment.
    db = firestore.Client()

    # Reference to the collection for notes. You might organize this by user ID or a central collection.
    notes_collection_ref = db.collection("user_onboarding_notes")

    # Convert the ProfileNote dataclass to a dictionary for Firestore
    note_data = {
        "user_id": payload.note.user_id,
        "note_content": payload.note.note_content,
        "timestamp": payload.note.timestamp,
        "author": payload.note.author,
        "category": payload.note.category,
    }

    # Add a new document to the collection
    doc_ref = notes_collection_ref.add(note_data)
    note_id = doc_ref[1].id # doc_ref is (timestamp, DocumentReference)

    return ProfileNoteStoreResponse(note_id=note_id, status="success")
