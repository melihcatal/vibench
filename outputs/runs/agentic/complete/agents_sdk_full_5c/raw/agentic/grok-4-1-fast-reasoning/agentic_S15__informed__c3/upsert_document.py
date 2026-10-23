from database_client import get_collection
from database_models import Document
from pymongo import ReturnDocument

def upsert_document(doc_id: str, document: Document, upsert: bool = True) -> Document:
    coll = get_collection()
    result = coll.find_one_and_update(
        {"_id": doc_id},
        {"$set": document},
        upsert=upsert,
        return_document=ReturnDocument.AFTER
    )
    return result