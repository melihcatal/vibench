import os
import datetime
from google.cloud import firestore
from identity_models import StoreProfileNoteRequest, StoreProfileNoteResponse


def profile_note_store(request: StoreProfileNoteRequest) -> StoreProfileNoteResponse:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    db = firestore.Client()

    notes_collection = db.collection("profile_notes")

    note_data = {
        "user_id": request.user_id,
        "note_content": request.note_content,
        "timestamp": datetime.datetime.now(datetime.timezone.utc),
        "metadata": request.metadata or {},
    }

    doc_ref = notes_collection.add(note_data)

    return StoreProfileNoteResponse(note_id=doc_ref[1].id, status="success")
