from typing import Optional
from database_client import get_collection, DatabaseClient
from database_models import DocumentRequest, UpdateResult, build_mongo_filter


@DatabaseClient.handle_mongo_error
def conditional_update(
    collection_name: str,
    document_id: str,
    updates: dict,
    expected_version: Optional[int] = None,
    partition_key: Optional[str] = None,
    additional_condition: Optional[dict] = None,
    connection_string: Optional[str] = None,
    db_name: Optional[str] = None,
) -> UpdateResult:
    request = DocumentRequest(
        collection=collection_name,
        document_id=document_id,
        data={},
        partition_key=partition_key,
        version=expected_version,
        condition=additional_condition,
    )
    collection = get_collection(
        collection_name, connection_string=connection_string, db_name=db_name
    )
    query_filter = build_mongo_filter(request)
    if expected_version is not None:
        query_filter["version"] = expected_version
    update_doc = {"$set": updates, "$inc": {"version": 1}}
    update_doc["$set"]["updated_at"] = (
        __import__("datetime").datetime.utcnow().isoformat()
    )
    result = collection.update_one(query_filter, update_doc)
    if result.matched_count == 0:
        current = collection.find_one({"_id": document_id})
        current_version = current.get("version") if current else None
        return UpdateResult(
            success=False,
            document_id=document_id,
            matched_count=0,
            modified_count=0,
            version=current_version,
            message="Condition not met or document not found",
        )
    updated_doc = collection.find_one({"_id": document_id})
    new_version = updated_doc.get("version", 0) if updated_doc else 0
    return UpdateResult(
        success=True,
        document_id=document_id,
        matched_count=result.matched_count,
        modified_count=result.modified_count,
        version=new_version,
        message="Document updated successfully",
    )


if __name__ == "__main__":
    result = conditional_update(
        collection_name="users",
        document_id="user_001",
        updates={"email": "alice_new@example.com"},
        expected_version=2,
        partition_key="users",
    )
    print(result)
