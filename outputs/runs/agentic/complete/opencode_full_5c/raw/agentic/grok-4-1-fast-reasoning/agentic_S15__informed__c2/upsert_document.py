from typing import Dict, Any
from pymongo import ReturnDocument
from database_client import get_mongodb_client, get_database, get_collection
from database_models import Document


def upsert_document(doc_id: str, document: Document) -> Document:
    client = get_mongodb_client()
    db = get_database(client)
    coll = get_collection(db)
    document = document.copy()
    document["_id"] = doc_id
    updated_doc = coll.find_one_and_replace(
        {"_id": doc_id}, document, upsert=True, return_document=ReturnDocument.AFTER
    )
    client.close()
    return updated_doc
