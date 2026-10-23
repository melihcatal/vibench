from pymongo import ReturnDocument
from database_client import get_collection
from database_models import Document
from typing import Dict, Any


def upsert_document(doc_id: str, document: Document) -> Document:
    document["_id"] = doc_id
    collection = get_collection()
    result = collection.find_one_and_replace(
        {"_id": doc_id}, document, upsert=True, return_document=ReturnDocument.AFTER
    )
    return result
