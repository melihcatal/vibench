import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId


def conditional_update(
    collection_name,
    document_id,
    update_data,
    condition_field=None,
    condition_value=None,
    version_field="_version",
):
    """
    Applies a conditional or version-aware update to one stored document in MongoDB Atlas.

    Args:
        collection_name: Name of the MongoDB collection
        document_id: Primary identifier for the document
        update_data: Dictionary of fields to update
        condition_field: Field name for conditional check (optional)
        condition_value: Expected value for conditional check (optional)
        version_field: Field name for version tracking (default: "_version")

    Returns:
        dict: Update result with success status
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

        # Build query for document identification
        query_id = document_id
        if isinstance(document_id, str) and ObjectId.is_valid(document_id):
            query_id = ObjectId(document_id)

        query = {"_id": query_id}

        # Add conditional check if provided
        if condition_field and condition_value is not None:
            query[condition_field] = condition_value

        # Prepare update operation
        # Increment version if version field exists
        update_operations = {"$set": update_data}
        if version_field:
            update_operations["$inc"] = {version_field: 1}

        # Perform conditional update
        result = collection.update_one(query, update_operations)

        client.close()

        if result.matched_count == 0:
            return {
                "success": False,
                "error": "Document not found or condition not met",
                "document_id": document_id,
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "condition": {"field": condition_field, "value": condition_value},
            }

        return {
            "success": True,
            "document_id": document_id,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "condition": {"field": condition_field, "value": condition_value},
        }

    except PyMongoError as e:
        return {
            "success": False,
            "error": f"MongoDB error: {str(e)}",
            "document_id": document_id,
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "document_id": document_id,
        }
