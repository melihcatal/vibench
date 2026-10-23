import os
from pymongo import MongoClient
from bson.objectid import ObjectId


def conditional_update(
    collection_name,
    document_id,
    update_data,
    condition_field=None,
    condition_value=None,
    version_field="_version",
):
    """
    Apply a conditional or version-aware update to one stored document.

    Args:
        collection_name: Name of the MongoDB collection
        document_id: Primary identifier for the document
        update_data: Data to update
        condition_field: Field to check for condition (optional)
        condition_value: Expected value for condition field (optional)
        version_field: Field name for version tracking (default: "_version")

    Returns:
        dict: Result with success status and update details
    """
    mongodb_uri = os.getenv("MONGODB_ATLAS_URI")
    if not mongodb_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required")

    client = MongoClient(mongodb_uri)
    db = client.get_database()
    collection = db[collection_name]

    try:
        query = {"_id": document_id}

        if condition_field and condition_value is not None:
            query[condition_field] = condition_value

        if version_field in update_data:
            current_version = update_data[version_field]
            query[version_field] = current_version
            update_data[version_field] = current_version + 1

        update_operation = {"$set": update_data}

        result = collection.update_one(query, update_operation)

        if result.matched_count == 0:
            return {
                "success": False,
                "error": "Document not found or condition not met",
                "matched_count": 0,
            }

        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "document_id": str(document_id),
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        client.close()
