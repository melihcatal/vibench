import os
from typing import Dict, Any
from database_client import MongoDBClient
from database_models import DocumentRequest, normalize_document

client = MongoDBClient()
collection = client.get_collection()

def upsert_document(document_id: str, payload: Dict[str, Any], partition_key: str = None) -> Dict[str, Any]:
    """Upsert a document into MongoDB Atlas by its primary identifier."""
    document = {
        "_id": document_id,
        **payload
    }
    if partition_key:
        document["partition_key"] = partition_key
    
    result = collection.replace_one({"_id": document_id}, document, upsert=True)
    if result.upserted_id:
        return {"status": "created", "document_id": document_id}
    else:
        return {"status": "updated", "document_id": document_id}