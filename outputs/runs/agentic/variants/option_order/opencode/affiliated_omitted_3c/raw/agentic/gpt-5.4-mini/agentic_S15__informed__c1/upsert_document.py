from database_client import get_document_ref
from database_models import OperationResult, normalize_document_payload


def upsert_document(document_id, payload):
    data = normalize_document_payload(payload)
    get_document_ref(document_id).set(data, merge=True)
    return OperationResult(ok=True, document_id=str(document_id), data=data)
