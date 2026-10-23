import os
from pymongo import MongoClient
from bson import ObjectId
from database_client import get_mongodb_client


def fetch_document(collection_name, document_id):
    """
    Fetch a document by identifier from MongoDB Atlas.

    Args:
        collection_name: Name of the MongoDB collection
        document_id: Primary identifier for the document

    Returns:
        dict: Document data if found, None otherwise
    """
    client = get_mongodb_client()
    db = client.get_database()
    collection = db[collection_name]

    try:
        # Try to fetch by _id
        document = collection.find_one({"_id": document_id})

        if document:
            # Convert ObjectId to string for JSON serialization
            if "_id" in document and isinstance(document["_id"], ObjectId):
                document["_id"] = str(document["_id"])
            return document
        else:
            return None
    except Exception as e:
        print(f"Error fetching document: {e}")
        return None
