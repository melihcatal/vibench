import os
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from database_client import get_mongodb_client


def upsert_document(collection_name, document_id, document_data):
    """
    Upsert a JSON document by its primary identifier.

    Args:
        collection_name: Name of the MongoDB collection
        document_id: Primary identifier for the document
        document_data: JSON document data to upsert

    Returns:
        dict: Result with success status and document ID
    """
    client = get_mongodb_client()
    db = client.get_database()
    collection = db[collection_name]

    # Ensure _id field is set
    document_data["_id"] = document_id

    try:
        result = collection.update_one(
            {"_id": document_id}, {"$set": document_data}, upsert=True
        )

        if result.upserted_id:
            return {
                "success": True,
                "operation": "insert",
                "document_id": str(result.upserted_id),
                "message": f"Document inserted with ID: {document_id}",
            }
        else:
            return {
                "success": True,
                "operation": "update",
                "document_id": document_id,
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "message": f"Document updated: {document_id}",
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to upsert document: {document_id}",
        }
