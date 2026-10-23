import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId


def query_documents(
    collection_name, field_name=None, field_value=None, partition_key=None, limit=100
):
    """
    Queries documents by a field value or partition-style key from MongoDB Atlas.

    Args:
        collection_name: Name of the MongoDB collection
        field_name: Field name to query by (optional)
        field_value: Field value to match (optional)
        partition_key: Partition key for sharded collections (optional)
        limit: Maximum number of documents to return

    Returns:
        dict: Query results with documents
    """
    try:
        # MongoDB Atlas connection string from environment variable
        mongo_uri = os.getenv("MONGODB_ATLAS_URI")
        if not mongo_uri:
            raise ValueError("MONGODB_ATLAS_URI environment variable not set")

        # Connect to MongoDB Atlas
        client = MongoClient(mongo_uri)
        db = client.get_database()
        collection = db[collection_name]

        # Build query based on provided parameters
        query = {}

        if field_name and field_value is not None:
            query[field_name] = field_value

        if partition_key:
            # For MongoDB, we can use the shard key if known
            # This is a simplified approach - actual shard key usage depends on cluster configuration
            query["_partition"] = partition_key

        # Execute query
        cursor = collection.find(query).limit(limit)
        documents = list(cursor)

        # Convert ObjectId to string for JSON serialization
        for doc in documents:
            if "_id" in doc and isinstance(doc["_id"], ObjectId):
                doc["_id"] = str(doc["_id"])

        client.close()

        return {
            "success": True,
            "documents": documents,
            "count": len(documents),
            "query": query,
            "limit": limit,
        }

    except PyMongoError as e:
        return {
            "success": False,
            "error": f"MongoDB error: {str(e)}",
            "query": {
                "field_name": field_name,
                "field_value": field_value,
                "partition_key": partition_key,
            },
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "query": {
                "field_name": field_name,
                "field_value": field_value,
                "partition_key": partition_key,
            },
        }
