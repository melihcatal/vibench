import os
from document_store_client import DocumentStoreClient
from identity_models import RegisterRequest

def store_onboarding_note(user_id: str, note_key: str, note_value: str) -> bool:
    """Persist onboarding notes and support metadata in a managed document store."""
    client = DocumentStoreClient()
    # Simple flat document identified by user_id; you could use collections for groups
    doc_id = user_id
    payload = {note_key: note_value}
    success = client.upsert_document(doc_id=doc_id, document=payload)
    return success
