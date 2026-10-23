import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError


def fetch_document(collection_name, document_id):
    """
    Fetch a document by identifier from MongoDB Atlas.

    Args:
        collection_name: Name of the MongoDB collection
        document_id: Primary identifier for the document

    Returns:
        dict: Document data if found, None otherwise
    """
    try:
        # MongoDB Atlas connection
        mongodb_uri = os.getenv("MONGODB_ATLAS_URI")
        if not mongodb_uri:
            raise ValueError("MONGODB_ATLAS_URI environment variable is required")

        client = MongoClient(mongodb_uri)
        db = client.get_database()
        collection = db[collection_name]

        # Fetch document by ID
        document = collection.find_one({"_id": document_id})

        client.close()

        if document:
            # Convert ObjectId to string for JSON serialization
            if "_id" in document:
                document["_id"] = str(document["_id"])
            return {"success": True, "document": document, "document_id": document_id}
        else:
            return {
                "success": False,
                "error": f"Document with ID {document_id} not found",
                "document_id": document_id,
            }

    except PyMongoError as e:
        return {"success": False, "error": str(e), "document_id": document_id}
    except Exception as e:
        return {"success": False, "error": str(e), "document_id": document_id}
