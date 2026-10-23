import os
from pymongo import MongoClient
from bson import ObjectId
from database_client import get_mongodb_client


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
        condition_field: Field to check for condition
        condition_value: Expected value for condition field
        version_field: Field name for version tracking

    Returns:
        dict: Result with success status and update details
    """
    client = get_mongodb_client()
    db = client.get_database()
    collection = db[collection_name]

    # Build the query filter
    query_filter = {"_id": document_id}

    # Add conditional check if provided
    if condition_field and condition_value is not None:
        query_filter[condition_field] = condition_value

    # For version-aware updates, include version check
    if version_field in update_data:
        current_version = update_data[version_field]
        query_filter[version_field] = current_version - 1  # Expect previous version
        update_data[version_field] = current_version

    try:
        result = collection.update_one(query_filter, {"$set": update_data})

        if result.matched_count == 0:
            return {
                "success": False,
                "matched_count": 0,
                "modified_count": 0,
                "message": "No document matched the condition",
            }

        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "message": f"Document updated: {document_id}",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to update document: {document_id}",
        }
