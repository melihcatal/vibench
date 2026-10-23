from typing import Any, Dict

from google.cloud import firestore

from identity_client import get_identity_settings

_PROVIDER_COLLECTION = "onboarding_notes"


def profile_note_store(user_id: str, note: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    settings = get_identity_settings()
    client = firestore.Client(project=settings.api_key)
    doc_ref = client.collection(_PROVIDER_COLLECTION).document(user_id)
    payload = {"note": note, "metadata": metadata}
    doc_ref.set(payload, merge=True)
    return {"stored": True, "collection": _PROVIDER_COLLECTION, "document_id": user_id}
