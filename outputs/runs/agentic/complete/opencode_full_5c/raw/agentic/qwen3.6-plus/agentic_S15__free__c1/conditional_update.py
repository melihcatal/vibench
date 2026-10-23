from database_client import get_collection
from database_models import ConditionalUpdateRequest, ConditionalUpdateResponse


def conditional_update(request: ConditionalUpdateRequest) -> ConditionalUpdateResponse:
    collection = get_collection()
    condition = request.to_mongo_condition()
    update = request.to_mongo_update()

    result = collection.update_one(condition, update)

    matched = result.matched_count > 0
    modified = result.modified_count > 0

    new_version = None
    if modified:
        updated_doc = collection.find_one({"_id": request.document_id})
        if updated_doc:
            new_version = updated_doc.get("version")

    return ConditionalUpdateResponse(
        document_id=request.document_id,
        matched=matched,
        modified=modified,
        new_version=new_version,
    )


def conditional_update_raw(
    document_id: str,
    updates: dict,
    expected_version: int = None,
    condition_field: str = None,
    condition_value=None,
) -> dict:
    request = ConditionalUpdateRequest(
        document_id=document_id,
        updates=updates,
        condition_field=condition_field,
        condition_value=condition_value,
        expected_version=expected_version,
    )
    response = conditional_update(request)
    return response.to_dict()


if __name__ == "__main__":
    result = conditional_update_raw(
        document_id="doc-001",
        updates={"status": "archived"},
        expected_version=2,
    )
    print(result)
