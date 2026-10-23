from pymongo import ReplaceOne
from database_client import get_collection
from database_models import (
    DocumentUpsertRequest,
    DocumentResponse,
    normalize_upsert_payload,
    normalize_document_response,
)


def upsert_document(request: DocumentUpsertRequest) -> DocumentResponse:
    collection = get_collection(request.collection)
    payload = normalize_upsert_payload(request)
    filter_doc = {"_id": request.document_id}
    collection.replace_one(filter_doc, payload, upsert=True)
    saved = collection.find_one(filter_doc)
    return normalize_document_response(saved, request.collection)
