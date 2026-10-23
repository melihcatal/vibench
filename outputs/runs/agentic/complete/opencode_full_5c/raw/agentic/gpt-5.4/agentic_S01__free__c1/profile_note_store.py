from identity_client import firestore_request
from identity_models import ProfileNoteStoreRequest, firestore_document


def profile_note_store(
    user_id: str,
    email: str,
    locale: str,
    notes: str,
    support_metadata: dict | None = None,
) -> dict:
    request = ProfileNoteStoreRequest(
        user_id=user_id,
        email=email,
        locale=locale,
        notes=notes,
        support_metadata=support_metadata or {},
    )
    document_id = request.user_id
    payload = firestore_document(
        user_id=request.user_id,
        email=request.email,
        locale=request.locale,
        notes=request.notes,
        support_metadata=request.support_metadata,
    )
    response = firestore_request("PATCH", f"onboarding_notes/{document_id}", payload)
    return {
        "document_name": response.get("name"),
        "user_id": request.user_id,
        "provider": "google-firestore",
    }
