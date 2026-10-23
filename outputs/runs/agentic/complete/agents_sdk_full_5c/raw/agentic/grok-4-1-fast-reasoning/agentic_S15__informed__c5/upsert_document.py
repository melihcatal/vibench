from database_client import get_collection
from database_models import normalize_for_upsert, Document
from typing import Dict, Any

def upsert_document(document_id: str, document_data: Dict[str, Any]) -> Document:
    coll = get_collection()
    normalized_data = normalize_for_upsert(document_data, document_id)
    coll.replace_one({"_id": document_id}, normalized_data, upsert=True)
    return coll.find_one({"_id": document_id})
