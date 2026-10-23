from database_client import get_collection
from database_models import UpdateResult


def conditional_update(
    document_id: str,
    updates: dict,
    expected_version: int = None,
    partition_key: str = "default",
) -> UpdateResult:
    collection = get_collection()

    query = {"document_id": document_id}
    if partition_key:
        query["partition_key"] = partition_key
    if expected_version is not None:
        query["version"] = expected_version

    existing = collection.find_one({"document_id": document_id})
    if existing is None:
        return UpdateResult(
            document_id=document_id,
            matched=False,
            modified=False,
            new_version=0,
        )

    current_version = existing.get("version", 0)
    update_payload = {"$set": {}}
    for key, value in updates.items():
        update_payload["$set"][f"data.{key}"] = value
    update_payload["$set"]["version"] = current_version + 1
    update_payload["$set"]["updated_at"] = existing.get("updated_at")

    result = collection.update_one(query, update_payload)

    if result.matched_count == 0:
        return UpdateResult(
            document_id=document_id,
            matched=False,
            modified=False,
            new_version=current_version,
        )

    updated_doc = collection.find_one({"document_id": document_id})
    new_version = (
        updated_doc.get("version", current_version + 1)
        if updated_doc
        else current_version + 1
    )

    return UpdateResult(
        document_id=document_id,
        matched=True,
        modified=result.modified_count > 0,
        new_version=new_version,
    )
