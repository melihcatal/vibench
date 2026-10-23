import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId


def fetch_document(collection_name, document_id):
    """
    Fetches a document by identifier from MongoDB Atlas.

    Args:
        collection_name: Name of the MongoDB collection
        document_id: Primary identifier for the document

    Returns:
        dict: Document data if found, None otherwise
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

        # Try to fetch document by _id
        # Handle both string IDs and ObjectId
        query_id = document_id
        if isinstance(document_id, str) and ObjectId.is_valid(document_id):
            query_id = ObjectId(document_id)

        document = collection.find_one({"_id": query_id})

        client.close()

        if document:
            # Convert ObjectId to string for JSON serialization
            if "_id" in document and isinstance(document["_id"], ObjectId):
                document["_id"] = str(document["_id"])
            return {"success": True, "document": document, "document_id": document_id}
        else:
            return {
                "success": False,
                "error": f"Document with ID {document_id} not found",
                "document_id": document_id,
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
