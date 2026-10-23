from identity_client import GoogleFirestoreClient
from identity_models import (
    StoreProfileNoteRequest,
    StoreProfileNoteResponse,
    ProfileNote,
)


def profile_note_store(request: StoreProfileNoteRequest) -> StoreProfileNoteResponse:
    client = GoogleFirestoreClient()
    doc_ref = client.db.collection("profile_notes").document()
    doc_ref.set(
        {
            "user_id": request.note.user_id,
            "timestamp": request.note.timestamp,
            "note": request.note.note,
            "metadata": request.note.metadata,
        }
    )
    return StoreProfileNoteResponse(document_id=doc_ref.id)
