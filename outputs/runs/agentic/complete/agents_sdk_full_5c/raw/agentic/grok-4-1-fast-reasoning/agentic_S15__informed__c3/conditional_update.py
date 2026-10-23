from database_client import get_collection
from database_models import Document, UpdateDict
from pymongo import ReturnDocument
from typing import Optional

def conditional_update(doc_id: str, updates: UpdateDict, expected_version: int) -> Optional[Document]:
    coll = get_collection()
    result = coll.find_one_and_update(
        {"_id": doc_id, "version": expected_version},
        {"$set": updates, "$inc": {"version": 1}},
        return_document=ReturnDocument.AFTER
    )
    return result