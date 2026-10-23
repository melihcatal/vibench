from pymongo import MongoClient, ReturnDocument
from pymongo.errors import PyMongoError
from database_client import get_mongodb_atlas_uri
from database_models import normalize_from_storage
from typing import Dict, Any


def upsert_document(doc_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    uri = get_mongodb_atlas_uri()
    client = MongoClient(uri)
    coll = client["testdb"]["documents"]
    result = coll.find_one_and_update(
        {"_id": doc_id},
        {"$set": {"data": data}, "$inc": {"version": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    client.close()
    return normalize_from_storage(result)
