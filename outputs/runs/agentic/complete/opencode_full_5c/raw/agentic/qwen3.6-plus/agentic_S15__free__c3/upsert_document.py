from typing import Optional
from pymongo import UpdateOne
from database_client import get_collection, DatabaseClient
from database_models import DocumentRequest, UpdateResult, prepare_upsert_payload


@DatabaseClient.handle_mongo_error
def upsert_document(
    collection_name: str,
    document_id: str,
    data: dict,
    partition_key: Optional[str] = None,
    connection_string: Optional[str] = None,
    db_name: Optional[str] = None,
) -> UpdateResult:
    request = DocumentRequest(
        collection=collection_name,
        document_id=document_id,
        data=data,
        partition_key=partition_key,
    )
    collection = get_collection(
        collection_name, connection_string=connection_string, db_name=db_name
    )
    payload = prepare_upsert_payload(request)
    query_filter = {"_id": request.document_id}
    if request.partition_key:
        query_filter["partition_key"] = request.partition_key
    update_doc = {"$set": payload, "$setOnInsert": {"version": 1}}
    update_doc["$inc"] = {"version": 1}
    result = collection.update_one(
        query_filter,
        update_doc,
        upsert=True,
    )
    if result.upserted_id:
        return UpdateResult(
            success=True,
            document_id=str(result.upserted_id),
            matched_count=result.matched_count,
            modified_count=result.modified_count,
            upserted_id=str(result.upserted_id),
            version=1,
            message="Document inserted",
        )
    current_doc = collection.find_one({"_id": document_id})
    version = current_doc.get("version", 0) if current_doc else 0
    return UpdateResult(
        success=True,
        document_id=document_id,
        matched_count=result.matched_count,
        modified_count=result.modified_count,
        version=version,
        message="Document updated",
    )


if __name__ == "__main__":
    result = upsert_document(
        collection_name="users",
        document_id="user_001",
        data={"name": "Alice", "email": "alice@example.com", "role": "admin"},
        partition_key="users",
    )
    print(result)
