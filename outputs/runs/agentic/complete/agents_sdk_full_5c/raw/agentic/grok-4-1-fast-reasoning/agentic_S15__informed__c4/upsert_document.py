from typing import Dict, Any
from database_client import get_collection
from database_models import Document

def upsert_document(document_id: str, document: Document) -> Document:
    document['_id'] = document_id
    collection = get_collection()
    collection.replace_one({'_id': document_id}, document, upsert=True)
    return document