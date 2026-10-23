from database_client import get_collection
from database_models import (
    ConditionalUpdateRequest,
    DocumentResponse,
    normalize_identifier,
)


def conditional_update(request: ConditionalUpdateRequest) -> DocumentResponse:
    collection = get_collection()
    document_id = normalize_identifier(request.document_id)
    query = {"id": document_id}
    if request.etag is not None:
        query["etag"] = request.etag
    if request.version_field:
        current = (
            collection.find_one(
                {"id": document_id}, {request.version_field: 1, "_id": 0}
            )
            or {}
        )
        if request.version_field in current:
            query[request.version_field] = current[request.version_field]
    update_doc = {"$set": dict(request.updates)}
    if request.version_field:
        update_doc["$inc"] = {request.version_field: 1}
    result = collection.find_one_and_update(query, update_doc, return_document=True)
    return DocumentResponse(
        ok=result is not None,
        document=result,
        error=None if result else "precondition failed",
    )
