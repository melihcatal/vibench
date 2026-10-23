from database_client import get_collection_ref
from database_models import build_document_response, normalize_identifier


def fetch_document(payload, config=None):
    config = config or {}
    document_id = normalize_identifier(payload)
    snapshot = get_collection_ref(config).document(document_id).get()
    return build_document_response(document_id, snapshot.to_dict() if snapshot.exists else None)
