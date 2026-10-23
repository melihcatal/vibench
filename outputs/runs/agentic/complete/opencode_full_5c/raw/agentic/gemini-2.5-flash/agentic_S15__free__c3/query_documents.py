import os
from typing import Any, List
from database_client import get_mongo_client, get_database, get_collection


def query_documents(
    collection_name: str, field_name: str, field_value: Any
) -> List[dict]:
    """
    Queries documents by a field value from a specified MongoDB collection.
    """
    client = get_mongo_client()
    database = get_database(client)
    collection = get_collection(database, collection_name)

    query = {field_name: field_value}
    cursor = collection.find(query)

    documents = []
    for doc in cursor:
        # MongoDB's _id can be an ObjectId, convert to string for consistent handling
        if "_id" in doc and not isinstance(doc["_id"], str):
            doc["_id"] = str(doc["_id"])
        documents.append(doc)

    client.close()
    return documents
