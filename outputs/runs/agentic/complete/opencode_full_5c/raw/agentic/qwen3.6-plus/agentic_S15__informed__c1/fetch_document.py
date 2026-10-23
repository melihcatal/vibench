from database_client import get_collection
from database_models import (
    DocumentFetchRequest,
    DocumentResponse,
    normalize_document_response,
)


def fetch_document(request: DocumentFetchRequest) -> DocumentResponse | None:
    collection = get_collection(request.collection)
    filter_doc = {"_id": request.document_id}
    raw_doc = collection.find_one(filter_doc)
    if raw_doc is None:
        return None
    return normalize_document_response(raw_doc, request.collection)
