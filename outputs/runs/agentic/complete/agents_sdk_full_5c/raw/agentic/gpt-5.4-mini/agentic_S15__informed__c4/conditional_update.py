from typing import Any, Dict

from pymongo import ReturnDocument

from database_client import get_collection
from database_models import ConditionalUpdateRequest, OperationResponse, normalize_for_update


def conditional_update(request: ConditionalUpdateRequest) -> Dict[str, Any]:
    collection = get_collection(request.db_name, request.collection_name)
    update_fields = normalize_for_update(request.update_fields)
    query = {"_id": str(request.document_id)}
    if request.expected_version is not None:
        query["version"] = request.expected_version
        update_fields["version"] = request.expected_version + 1
    updated = collection.find_one_and_update(query, {"$set": update_fields}, return_document=ReturnDocument.AFTER)
    return OperationResponse(ok=updated is not None, provider="MongoDB Atlas", data={"document": updated}).__dict__
