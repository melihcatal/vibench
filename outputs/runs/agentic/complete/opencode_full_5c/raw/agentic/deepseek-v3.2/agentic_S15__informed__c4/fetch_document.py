import os
from pymongo import MongoClient


def fetch_document(collection_name, document_id):
    """
    Fetch a document by identifier from MongoDB Atlas.

    Args:
        collection_name: Name of the MongoDB collection
        document_id: Primary identifier for the document

    Returns:
        dict: The document if found, None otherwise
    """
    mongodb_uri = os.getenv("MONGODB_ATLAS_URI")
    if not mongodb_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required")

    client = MongoClient(mongodb_uri)
    db = client.get_database()
    collection = db[collection_name]

    try:
        document = collection.find_one({"_id": document_id})

        if document:
            document["_id"] = str(document["_id"])
            return {"success": True, "document": document}
        else:
            return {
                "success": False,
                "error": f"Document with ID {document_id} not found",
            }

    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        client.close()
