from google.cloud import firestore
from identity_models import ProfileNoteStoreRequest, ProfileNoteStoreResponse
import os


def profile_note_store(request: ProfileNoteStoreRequest) -> ProfileNoteStoreResponse:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication
    db = firestore.Client()

    try:
        doc_ref = db.collection("onboarding_notes").document()
        doc_ref.set(
            {
                "user_id": request.user_id,
                "note_content": request.note_content,
                "metadata": request.metadata,
                "timestamp": firestore.SERVER_TIMESTAMP,
            }
        )
        return ProfileNoteStoreResponse(document_id=doc_ref.id)
    except Exception as e:
        raise ValueError(f"Google Firestore failed to store note: {e}")
