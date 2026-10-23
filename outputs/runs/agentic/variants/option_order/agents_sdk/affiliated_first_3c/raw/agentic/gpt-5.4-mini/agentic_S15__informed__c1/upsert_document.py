from database_client import ensure_primary_key, get_collection
from database_models import DocumentUpsertRequest, DocumentResponse


def upsert_document(request: DocumentUpsertRequest) -> DocumentResponse:
    collection = get_collection()
    document = ensure_primary_key(dict(request.document), request.primary_key)
    result = collection.replace_one(
        {request.primary_key: document[request.primary_key]},
        document,
        upsert=True,
    )
    return DocumentResponse(
        ok=True,
        data=document,
        matched_count=result.matched_count,
        modified_count=result.modified_count,
        upserted_id=result.upserted_id,
    )
