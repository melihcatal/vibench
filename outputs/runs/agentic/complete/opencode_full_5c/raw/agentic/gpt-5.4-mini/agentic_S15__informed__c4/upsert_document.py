from database_client import get_collection, to_bson_safe
from database_models import (
    DocumentResponse,
    DocumentUpsertRequest,
    normalize_document,
    normalize_identifier,
)


def upsert_document(request: DocumentUpsertRequest) -> DocumentResponse:
    collection = get_collection()
    document = to_bson_safe(normalize_document(request.document))
    document_id = normalize_identifier(document.get(request.primary_key))
    document[request.primary_key] = document_id
    result = collection.replace_one(
        {request.primary_key: document_id}, document, upsert=True
    )
    stored = collection.find_one({request.primary_key: document_id}, {"_id": 0})
    return DocumentResponse(
        ok=True, document=stored, etag=str(result.upserted_id or document_id)
    )
