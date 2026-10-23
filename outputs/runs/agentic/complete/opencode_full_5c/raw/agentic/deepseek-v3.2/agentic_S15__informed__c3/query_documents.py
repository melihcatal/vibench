import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError


def query_documents(collection_name, field_name, field_value, limit=100):
    """
    Query documents by a field value from MongoDB Atlas.

    Args:
        collection_name: Name of the MongoDB collection
        field_name: Field name to query by
        field_value: Field value to match
        limit: Maximum number of documents to return

    Returns:
        dict: Query results with matching documents
    """
    try:
        # MongoDB Atlas connection
        mongodb_uri = os.getenv("MONGODB_ATLAS_URI")
        if not mongodb_uri:
            raise ValueError("MONGODB_ATLAS_URI environment variable is required")

        client = MongoClient(mongodb_uri)
        db = client.get_database()
        collection = db[collection_name]

        # Build query
        query = {field_name: field_value}

        # Execute query
        cursor = collection.find(query).limit(limit)
        documents = list(cursor)

        # Convert ObjectId to string for JSON serialization
        for doc in documents:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])

        client.close()

        return {
            "success": True,
            "documents": documents,
            "count": len(documents),
            "field_name": field_name,
            "field_value": field_value,
            "limit": limit,
        }

    except PyMongoError as e:
        return {
            "success": False,
            "error": str(e),
            "field_name": field_name,
            "field_value": field_value,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "field_name": field_name,
            "field_value": field_value,
        }
