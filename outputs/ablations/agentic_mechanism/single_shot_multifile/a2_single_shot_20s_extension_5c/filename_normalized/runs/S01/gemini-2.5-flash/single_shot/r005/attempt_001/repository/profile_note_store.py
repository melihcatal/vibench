from identity_client import config
from identity_models import NoteStoreRequest, NoteStoreResponse
from google.cloud import firestore
from google.cloud.firestore import Client as FirestoreClient


def profile_note_store(request: NoteStoreRequest) -> NoteStoreResponse:
    """
    Persists onboarding notes and support metadata in Google Cloud Firestore.
    """
    db: FirestoreClient = config.firestore_client

    try:
        user_notes_ref = db.collection("users").document(request.user_id).collection("notes")

        update_time, doc_ref = user_notes_ref.add({
            "note_type": request.note_type,
            "content": request.content,
            "timestamp": firestore.SERVER_TIMESTAMP
        })

        return NoteStoreResponse(
            document_id=doc_ref.id,
            status="success"
        )
    except Exception as e:
        raise RuntimeError(f"Failed to store note in Firestore: {e}")
