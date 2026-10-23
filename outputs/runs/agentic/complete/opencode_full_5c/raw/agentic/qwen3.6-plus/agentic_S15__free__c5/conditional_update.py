from database_client import get_collection
from database_models import ConditionalUpdateRequest, ConditionalUpdateResponse


def conditional_update(request: ConditionalUpdateRequest) -> ConditionalUpdateResponse:
    collection = get_collection()
    query_filter = {"_id": request.document_id}

    if request.expected_version is not None:
        query_filter["version"] = request.expected_version

    if request.condition:
        query_filter.update(request.condition)

    update_ops = {"$set": request.updates, "$inc": {"version": 1}}
    result = collection.update_one(query_filter, update_ops)

    if result.matched_count == 0:
        return ConditionalUpdateResponse(
            document_id=request.document_id,
            updated=False,
            error="Condition not met or document not found",
        )

    updated_doc = collection.find_one({"_id": request.document_id})
    return ConditionalUpdateResponse(
        document_id=request.document_id,
        updated=True,
        new_version=updated_doc.get("version", 0),
    )
