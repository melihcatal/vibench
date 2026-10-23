from identity_client import (
    FIRESTORE_PROVIDER,
    get_firestore_client,
    get_firestore_collection,
)
from identity_models import ProfileNoteStoreRequest, ProfileNoteStoreResponse


def profile_note_store(
    user_id: str,
    email: str,
    locale: str,
    notes: list[str],
    support_metadata: dict | None = None,
) -> dict:
    request = ProfileNoteStoreRequest(
        user_id=user_id,
        email=email,
        locale=locale,
        notes=notes,
        support_metadata=support_metadata or {},
    )
    client = get_firestore_client()
    collection = client.collection(get_firestore_collection())
    document = request.to_document()
    doc_ref = collection.document(request.user_id)
    doc_ref.set(document, merge=True)
    result = ProfileNoteStoreResponse(
        provider=FIRESTORE_PROVIDER,
        document_id=doc_ref.id,
        status="stored",
    )
    return result.to_dict()
