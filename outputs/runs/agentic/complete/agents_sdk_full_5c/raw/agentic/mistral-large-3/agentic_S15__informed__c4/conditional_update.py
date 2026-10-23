from typing import Dict, Any, Optional
from pymongo import ReturnDocument
from database_client import MongoDBClient
from database_models import DocumentResponse, normalize_document

client = MongoDBClient()
collection = client.get_collection()

def conditional_update(document_id: str, update_payload: Dict[str, Any], current_version: Optional[int] = None) -> Optional[DocumentResponse]:
    """Apply a conditional or version-aware update to a document in MongoDB Atlas."""
    query = {"_id": document_id}
    if current_version is not None:
        query["version"] = current_version
    
    update = {
        "$set": update_payload,
        "$inc": {"version": 1}
    }
    
    document = collection.find_one_and_update(
        query,
        update,
        return_document=ReturnDocument.AFTER
    )
    
    if document:
        return normalize_document(document)
    return None