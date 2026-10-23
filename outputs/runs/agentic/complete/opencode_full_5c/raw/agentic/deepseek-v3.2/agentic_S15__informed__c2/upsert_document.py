import os
from pymongo import MongoClient, UpdateOne
from pymongo.errors import PyMongoError


def upsert_document(collection_name, document_id, document_data):
    """
    Upserts a JSON document by its primary identifier into MongoDB Atlas.

    Args:
        collection_name: Name of the MongoDB collection
        document_id: Primary identifier for the document
        document_data: JSON document data to upsert

    Returns:
        dict: Result containing success status and document ID
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

        # Prepare document with _id field
        document = document_data.copy()
        document["_id"] = document_id

        # Perform upsert operation
        result = collection.update_one(
            {"_id": document_id}, {"$set": document}, upsert=True
        )

        client.close()

        if result.upserted_id:
            return {
                "success": True,
                "operation": "insert",
                "document_id": str(result.upserted_id),
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
            }
        else:
            return {
                "success": True,
                "operation": "update",
                "document_id": document_id,
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
            }

    except PyMongoError as e:
        return {"success": False, "error": f"MongoDB error: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}
