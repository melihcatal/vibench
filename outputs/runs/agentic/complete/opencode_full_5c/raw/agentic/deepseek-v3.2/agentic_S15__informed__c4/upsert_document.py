import os
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


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
    mongodb_uri = os.getenv("MONGODB_ATLAS_URI")
    if not mongodb_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required")

    client = MongoClient(mongodb_uri)
    db = client.get_database()
    collection = db[collection_name]

    document_data["_id"] = document_id

    try:
        result = collection.replace_one(
            {"_id": document_id}, document_data, upsert=True
        )

        if result.upserted_id:
            return {
                "success": True,
                "action": "inserted",
                "document_id": str(result.upserted_id),
            }
        else:
            return {
                "success": True,
                "action": "updated",
                "document_id": str(document_id),
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
            }

    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        client.close()
