import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError


def conditional_update(
    collection_name, document_id, update_data, condition_field, condition_value
):
    """
    Apply a conditional update to one stored document in MongoDB Atlas.

    Args:
        collection_name: Name of the MongoDB collection
        document_id: Primary identifier for the document
        update_data: Data to update
        condition_field: Field name for the condition
        condition_value: Expected value for the condition

    Returns:
        dict: Update result with status
    """
    try:
        # MongoDB Atlas connection
        mongodb_uri = os.getenv("MONGODB_ATLAS_URI")
        if not mongodb_uri:
            raise ValueError("MONGODB_ATLAS_URI environment variable is required")

        client = MongoClient(mongodb_uri)
        db = client.get_database()
        collection = db[collection_name]

        # Build query with condition
        query = {"_id": document_id, condition_field: condition_value}

        # Execute conditional update
        result = collection.update_one(query, {"$set": update_data})

        client.close()

        if result.matched_count > 0:
            return {
                "success": True,
                "document_id": document_id,
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "condition_met": True,
                "condition_field": condition_field,
                "condition_value": condition_value,
            }
        else:
            return {
                "success": False,
                "document_id": document_id,
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "condition_met": False,
                "condition_field": condition_field,
                "condition_value": condition_value,
                "error": "Condition not met or document not found",
            }

    except PyMongoError as e:
        return {
            "success": False,
            "error": str(e),
            "document_id": document_id,
            "condition_field": condition_field,
            "condition_value": condition_value,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "document_id": document_id,
            "condition_field": condition_field,
            "condition_value": condition_value,
        }
