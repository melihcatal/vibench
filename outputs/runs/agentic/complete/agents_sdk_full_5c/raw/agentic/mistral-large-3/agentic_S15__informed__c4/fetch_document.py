from typing import Optional, Dict, Any
from database_client import MongoDBClient
from database_models import DocumentResponse, normalize_document

client = MongoDBClient()
collection = client.get_collection()

def fetch_document(document_id: str) -> Optional[DocumentResponse]:
    """Fetch a document from MongoDB Atlas by its identifier."""
    document = collection.find_one({"_id": document_id})
    if document:
        return normalize_document(document)
    return None