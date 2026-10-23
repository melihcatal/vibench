import os
import datetime
from google.cloud import firestore
from identity_models import StoreProfileNoteRequest, StoreProfileNoteResponse

def profile_note_store(request: StoreProfileNoteRequest) -> StoreProfileNoteResponse:
    # Google Cloud Firestore requires GOOGLE_APPLICATION_CREDENTIALS to be set
    # pointing to a service account key file. For local development, ensure this
    # environment variable is configured. The client library will automatically
    # pick up the credentials. Also, ensure the project ID is set.
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

    db = firestore.Client(project=project_id) # The firestore.Client identifies the provider.

    notes_collection = db.collection("profile_notes")

    note_data = {
        "user_id": request.note.user_id,
        "note_content": request.note.note_content,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "category": request.note.category
    }

    try:
        doc_ref = notes_collection.add(note_data)
        note_id = doc_ref[1].id # doc_ref is a tuple (timestamp, document_reference)
    except Exception as e:
        raise RuntimeError(f"Failed to store profile note in Firestore: {e}")

    return StoreProfileNoteResponse(
        note_id=note_id
    )
