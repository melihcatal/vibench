from database_client import get_document_ref
from database_models import DocumentRecord, OperationResult


def fetch_document(document_id):
    snapshot = get_document_ref(document_id).get()
    if not snapshot.exists:
        return OperationResult(ok=False, document_id=str(document_id))
    return DocumentRecord(document_id=str(document_id), data=snapshot.to_dict() or {})
