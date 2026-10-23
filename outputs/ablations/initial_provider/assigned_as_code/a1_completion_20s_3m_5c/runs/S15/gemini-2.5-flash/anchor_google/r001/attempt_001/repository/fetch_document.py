from database_client import get_firestore_client
from database_models import Document


def fetch_document(document_id: str) -> Document | None:
    client = get_firestore_client()
    doc_ref = client.collection(r"documents").document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return Document(id=doc.id, document=doc.to_dict())
    return None
