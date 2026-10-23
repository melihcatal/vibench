from pymongo import ReturnDocument
from database_client import get_collection
from database_models import (
    ConditionalUpdateRequest,
    UpdateResponse,
    build_update_set_fields,
)


def conditional_update(request: ConditionalUpdateRequest) -> UpdateResponse:
    collection = get_collection()

    filter_criteria = {"document_id": request.document_id}
    if request.partition_key:
        filter_criteria["partition_key"] = request.partition_key

    if request.condition_field is not None and request.condition_value is not None:
        filter_criteria[request.condition_field] = request.condition_value

    set_fields = build_update_set_fields(request)

    existing = collection.find_one({"document_id": request.document_id})
    current_version = existing.get("version", 0) if existing else 0

    result = collection.find_one_and_update(
        filter_criteria,
        {"$set": set_fields, "$inc": {"version": 1}},
        return_document=ReturnDocument.AFTER,
    )

    if result is None:
        condition_met = (
            request.condition_field is None or request.condition_value is None
        )
        if condition_met:
            condition_met = False
        return UpdateResponse(
            document_id=request.document_id,
            matched=False,
            modified=False,
            version=current_version,
            condition_met=condition_met,
        )

    return UpdateResponse(
        document_id=request.document_id,
        matched=True,
        modified=True,
        version=result.get("version", current_version + 1),
        condition_met=True,
    )
