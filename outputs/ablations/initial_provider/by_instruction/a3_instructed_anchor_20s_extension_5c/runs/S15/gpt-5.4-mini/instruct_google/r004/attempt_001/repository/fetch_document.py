from database_client import document_ref
from database_models import normalize_document_id, DocumentResult


def fetch_document(document_id):
    document_id = normalize_document_id(document_id)
    snapshot = document_ref(document_id).get()
    data = snapshot.to_dict() if snapshot.exists else {}
    return DocumentResult(id=document_id, data=data, exists=snapshot.exists)
