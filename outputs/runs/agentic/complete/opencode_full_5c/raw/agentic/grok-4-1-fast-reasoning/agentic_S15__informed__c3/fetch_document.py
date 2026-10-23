from pymongo import MongoClient
from database_client import get_mongodb_atlas_uri
from database_models import normalize_from_storage
from typing import Dict, Any, Optional


def fetch_document(doc_id: str) -> Optional[Dict[str, Any]]:
    uri = get_mongodb_atlas_uri()
    client = MongoClient(uri)
    coll = client["testdb"]["documents"]
    doc = coll.find_one({"_id": doc_id})
    client.close()
    return normalize_from_storage(doc)
