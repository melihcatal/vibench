import os
from database_client import get_mongo_client, get_database, get_collection
from database_models import deserialize_document


def fetch_document(
    collection_name: str, document_id: str, id_field: str = "_id"
) -> dict | None:
    """
    Fetches a document by identifier from a specified MongoDB collection.
    """
    client = get_mongo_client()
    database = get_database(client)
    collection = get_collection(database, collection_name)

    document = collection.find_one({id_field: document_id})
    client.close()

    if document:
        # MongoDB's _id can be an ObjectId, convert to string for consistent handling
        if "_id" in document and not isinstance(document["_id"], str):
            document["_id"] = str(document["_id"])
        return document
    return None
