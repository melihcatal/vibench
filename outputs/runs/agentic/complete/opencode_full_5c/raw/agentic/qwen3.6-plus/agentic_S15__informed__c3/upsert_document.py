import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from database_client import get_mongo_client, get_database_name, get_collection_name
from database_models import UpsertRequest, UpsertResponse


def upsert_document(
    doc_id: str, data: dict, extra_fields: dict | None = None
) -> UpsertResponse:
    client = get_mongo_client()
    db_name = get_database_name()
    collection_name = get_collection_name()

    try:
        db = client[db_name]
        collection = db[collection_name]

        document = {"_id": doc_id, "data": data}
        if extra_fields:
            document.update(extra_fields)

        result = collection.replace_one({"_id": doc_id}, document, upsert=True)

        if result.upserted_id:
            return UpsertResponse(
                document_id=str(result.upserted_id),
                action="inserted",
                matched_count=result.matched_count,
                modified_count=result.modified_count,
            )
        else:
            return UpsertResponse(
                document_id=doc_id,
                action="updated",
                matched_count=result.matched_count,
                modified_count=result.modified_count,
            )
    except PyMongoError as e:
        return UpsertResponse(
            document_id=doc_id,
            action="error",
            matched_count=0,
            modified_count=0,
            error=str(e),
        )
    finally:
        client.close()


if __name__ == "__main__":
    sample_data = {
        "title": "Sample Document",
        "content": "Hello World",
        "status": "active",
    }
    response = upsert_document("doc-001", sample_data)
    print(response)
