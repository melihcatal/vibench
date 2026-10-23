from database_client import get_collection
from database_models import (
    ConditionalUpdateRequest,
    UpdateResponse,
    normalize_document_response,
)


def conditional_update(request: ConditionalUpdateRequest) -> UpdateResponse:
    collection = get_collection(request.collection)
    filter_doc = {
        "_id": request.document_id,
        request.condition_field: request.condition_value,
    }
    result = collection.update_one(filter_doc, {"$set": request.updates})
    matched = result.matched_count > 0
    modified = result.modified_count > 0
    updated_doc = None
    if modified:
        updated_doc = collection.find_one({"_id": request.document_id})
    version = None
    if updated_doc:
        version = updated_doc.get("_version", updated_doc.get("version"))
    return UpdateResponse(
        document_id=request.document_id,
        matched=matched,
        modified=modified,
        version=version,
    )
