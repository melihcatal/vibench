from database_client import get_db_client
from bson import ObjectId
from typing import Optional, Dict, Any


def fetch_document(document_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetches a document by its ID from MongoDB Atlas.
    """
    client = get_db_client()
    document = client.find_one({"_id": ObjectId(document_id)})
    if document:
        document["_id"] = str(document["_id"])
    return document
