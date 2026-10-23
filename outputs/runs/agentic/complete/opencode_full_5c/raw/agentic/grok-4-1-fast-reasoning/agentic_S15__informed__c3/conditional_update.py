from pymongo import MongoClient
from database_client import get_mongodb_atlas_uri
from typing import Dict, Any


def conditional_update(
    doc_id: str, updates: Dict[str, Any], expected_version: int
) -> bool:
    uri = get_mongodb_atlas_uri()
    client = MongoClient(uri)
    coll = client["testdb"]["documents"]
    full_updates = {**updates, "version": expected_version + 1}
    result = coll.update_one(
        {"_id": doc_id, "version": expected_version}, {"$set": full_updates}
    )
    client.close()
    return result.matched_count > 0
