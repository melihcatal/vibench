import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from database_client import get_mongo_client, get_database_name, get_collection_name
from database_models import FetchRequest, FetchResponse


def fetch_document(doc_id: str) -> FetchResponse:
    client = get_mongo_client()
    db_name = get_database_name()
    collection_name = get_collection_name()

    try:
        db = client[db_name]
        collection = db[collection_name]

        document = collection.find_one({"_id": doc_id})

        if document:
            doc_data = document.get("data", {})
            doc_data["_id"] = str(document["_id"])
            if "created_at" in document:
                doc_data["created_at"] = document["created_at"]
            if "updated_at" in document:
                doc_data["updated_at"] = document["updated_at"]
            if "version" in document:
                doc_data["version"] = document["version"]

            return FetchResponse(document_id=doc_id, data=doc_data, found=True)
        else:
            return FetchResponse(document_id=doc_id, data=None, found=False)
    except PyMongoError as e:
        return FetchResponse(document_id=doc_id, data=None, found=False, error=str(e))
    finally:
        client.close()


if __name__ == "__main__":
    response = fetch_document("doc-001")
    print(response)
