import os
from pymongo import MongoClient


def query_documents(
    collection_name, field_name=None, field_value=None, partition_key=None, limit=100
):
    """
    Query documents by a field value or partition-style key.

    Args:
        collection_name: Name of the MongoDB collection
        field_name: Field name to query by (optional)
        field_value: Field value to match (optional)
        partition_key: Partition key value (optional)
        limit: Maximum number of documents to return

    Returns:
        list: List of matching documents
    """
    mongodb_uri = os.getenv("MONGODB_ATLAS_URI")
    if not mongodb_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required")

    client = MongoClient(mongodb_uri)
    db = client.get_database()
    collection = db[collection_name]

    try:
        query = {}

        if field_name and field_value is not None:
            query[field_name] = field_value

        if partition_key:
            query["partition_key"] = partition_key

        cursor = collection.find(query).limit(limit)
        documents = []

        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            documents.append(doc)

        return {"success": True, "documents": documents, "count": len(documents)}

    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        client.close()
