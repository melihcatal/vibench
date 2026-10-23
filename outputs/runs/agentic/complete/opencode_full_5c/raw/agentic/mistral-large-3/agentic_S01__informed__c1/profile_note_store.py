from typing import Dict, Any, Optional
import os
from google.cloud import firestore
from identity_models import ProfileNoteStoreRequest, ProfileNoteStoreResponse

# Initialize Google Firestore client with provider-specific credentials
firestore_client = firestore.Client()


def profile_note_store(request: ProfileNoteStoreRequest) -> ProfileNoteStoreResponse:
    """
    Persists onboarding notes and support metadata in Google Firestore.
    """
    try:
        doc_ref = firestore_client.collection("onboarding_notes").document(
            request.user_id
        )
        doc_ref.set(
            {
                "notes": request.notes,
                "metadata": request.metadata,
                "updated_at": firestore.SERVER_TIMESTAMP,
            }
        )

        return ProfileNoteStoreResponse(success=True, document_id=doc_ref.id)
    except Exception as e:
        return ProfileNoteStoreResponse(success=False, error=str(e))
