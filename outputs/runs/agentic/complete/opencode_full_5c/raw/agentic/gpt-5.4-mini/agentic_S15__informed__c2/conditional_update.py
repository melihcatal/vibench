from database_client import get_collection
from database_models import ConditionalUpdateRequest, serialize_document


def conditional_update(payload):
    request = ConditionalUpdateRequest.from_payload(payload)
    collection = get_collection()
    update = {"$set": serialize_document(request.updates)}
    if request.version_field and request.expected_version is not None:
        query = {request.id_field: request.document_id, request.version_field: request.expected_version}
        update.setdefault("$inc", {})[request.version_field] = 1
    else:
        query = {request.id_field: request.document_id}
    return collection.find_one_and_update(query, update, return_document=True)
