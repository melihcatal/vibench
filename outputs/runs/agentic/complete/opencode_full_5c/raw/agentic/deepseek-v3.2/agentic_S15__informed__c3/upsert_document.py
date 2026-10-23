import os
from pymongo import MongoClient, UpdateOne
from pymongo.errors import PyMongoError


def upsert_document(collection_name, document_id, document_data):
    """
    Upsert a JSON document by its primary identifier.

    Args:
        collection_name: Name of the MongoDB collection
        document_id: Primary identifier for the document
        document_data: JSON document data to upsert

    Returns:
        dict: Result containing success status and document ID
    """
    try:
        # MongoDB Atlas connection
        mongodb_uri = os.getenv("MONGODB_ATLAS_URI")
        if not mongodb_uri:
            raise ValueError("MONGODB_ATLAS_URI environment variable is required")

        client = MongoClient(mongodb_uri)
        db = client.get_database()
        collection = db[collection_name]

        # Create upsert operation
        document_data["_id"] = document_id
        result = collection.update_one(
            {"_id": document_id}, {"$set": document_data}, upsert=True
        )

        client.close()

        return {
            "success": True,
            "document_id": document_id,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "upserted_id": result.upserted_id,
        }

    except PyMongoError as e:
        return {"success": False, "error": str(e), "document_id": document_id}
    except Exception as e:
        return {"success": False, "error": str(e), "document_id": document_id}
