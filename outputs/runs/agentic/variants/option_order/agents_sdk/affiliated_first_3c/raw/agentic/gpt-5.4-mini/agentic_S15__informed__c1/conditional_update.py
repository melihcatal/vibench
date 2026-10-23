from database_client import get_collection
from database_models import ConditionalUpdateRequest, DocumentResponse


def conditional_update(request: ConditionalUpdateRequest) -> DocumentResponse:
    collection = get_collection()
    filter_doc = {request.primary_key: request.identifier}
    if request.expected_version is not None:
        filter_doc[request.version_field] = request.expected_version
    updates = dict(request.updates)
    if request.expected_version is not None:
        updates[request.version_field] = request.expected_version + 1
    result = collection.update_one(filter_doc, {"$set": updates})
    if result.matched_count == 0:
        return DocumentResponse(ok=False, error="Conditional update failed")
    return DocumentResponse(ok=True, matched_count=result.matched_count, modified_count=result.modified_count)
