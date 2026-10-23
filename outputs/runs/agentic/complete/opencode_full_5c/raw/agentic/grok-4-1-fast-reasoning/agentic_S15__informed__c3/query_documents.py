from pymongo import MongoClient
from database_client import get_mongodb_atlas_uri
from database_models import normalize_from_storage
from typing import Dict, Any, List


def query_documents(field_path: str, value: Any) -> List[Dict[str, Any]]:
    uri = get_mongodb_atlas_uri()
    client = MongoClient(uri)
    coll = client["testdb"]["documents"]
    docs = coll.find({f"data.{field_path}": value})
    result = [normalize_from_storage(doc) for doc in docs]
    client.close()
    return result
