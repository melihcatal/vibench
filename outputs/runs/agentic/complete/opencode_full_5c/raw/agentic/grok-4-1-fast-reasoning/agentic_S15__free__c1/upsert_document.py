import os
from datetime import datetime
from typing import Any, Dict
from database_client import get_mongo_client, get_database, get_documents_collection
from database_models import Document


def upsert_document(doc_id: str, data: Dict[str, Any]) -> Document:
    client = get_mongo_client()
    db = get_database(client)
    collection = get_documents_collection(db)
    now = datetime.utcnow().isoformat()
    current_doc = collection.find_one({"doc_id": doc_id})
    if current_doc:
        version = current_doc["version"] + 1
        doc = {
            "doc_id": doc_id,
            "data": data,
            "version": version,
            "updated_at": now,
        }
    else:
        version = 1
        doc = {
            "doc_id": doc_id,
            "data": data,
            "version": version,
            "created_at": now,
            "updated_at": now,
        }
    collection.replace_one({"doc_id": doc_id}, doc, upsert=True)
    return collection.find_one({"doc_id": doc_id})
