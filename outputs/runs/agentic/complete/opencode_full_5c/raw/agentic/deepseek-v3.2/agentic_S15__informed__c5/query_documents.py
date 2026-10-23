import os
from pymongo import MongoClient
from bson import ObjectId
from database_client import get_mongodb_client


def query_documents(
    collection_name, field_name=None, field_value=None, partition_key=None, limit=100
):
    """
    Query documents by field value or partition-style key.

    Args:
        collection_name: Name of the MongoDB collection
        field_name: Field name to query by
        field_value: Field value to match
        partition_key: Partition key for filtering
        limit: Maximum number of documents to return

    Returns:
        list: List of matching documents
    """
    client = get_mongodb_client()
    db = client.get_database()
    collection = db[collection_name]

    query_filter = {}

    if field_name and field_value is not None:
        query_filter[field_name] = field_value

    if partition_key:
        # For MongoDB, we can use partition key as a field filter
        # This assumes partition_key is a dict with field:value pairs
        if isinstance(partition_key, dict):
            query_filter.update(partition_key)
        else:
            # If it's a simple value, use it as a filter on a default field
            query_filter["partition"] = partition_key

    try:
        cursor = collection.find(query_filter).limit(limit)
        documents = []

        for doc in cursor:
            # Convert ObjectId to string for JSON serialization
            if "_id" in doc and isinstance(doc["_id"], ObjectId):
                doc["_id"] = str(doc["_id"])
            documents.append(doc)

        return documents
    except Exception as e:
        print(f"Error querying documents: {e}")
        return []
