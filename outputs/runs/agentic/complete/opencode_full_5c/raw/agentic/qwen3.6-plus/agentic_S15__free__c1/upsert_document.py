import os
from database_client import (
    get_collection,
    MONGODB_ATLAS_DATABASE,
    MONGODB_ATLAS_COLLECTION,
)
from database_models import DocumentUpsertRequest, DocumentFetchResponse
from pymongo.errors import DuplicateKeyError, WriteError


def upsert_document(request: DocumentUpsertRequest) -> DocumentFetchResponse:
    collection = get_collection()
    mongo_doc = request.to_mongo_document()

    existing = collection.find_one({"_id": request.document_id})
    if existing is None:
        mongo_doc["created_at"] = mongo_doc["updated_at"]
        if "version" not in mongo_doc:
            mongo_doc["version"] = 1
        collection.insert_one(mongo_doc)
    else:
        current_version = existing.get("version", 0)
        mongo_doc["version"] = current_version + 1
        mongo_doc["created_at"] = existing.get("created_at")
        collection.replace_one(
            {"_id": request.document_id},
            mongo_doc,
        )

    updated = collection.find_one({"_id": request.document_id})
    return DocumentFetchResponse.from_mongo_document(updated)


def upsert_document_raw(
    document_id: str, data: dict, partition_key: str = None
) -> dict:
    request = DocumentUpsertRequest(
        document_id=document_id,
        data=data,
        partition_key=partition_key,
    )
    response = upsert_document(request)
    return response.to_dict()


if __name__ == "__main__":
    result = upsert_document_raw(
        document_id="doc-001",
        data={
            "title": "Sample Document",
            "content": "Hello from MongoDB Atlas",
            "status": "active",
        },
        partition_key="default",
    )
    print(result)
