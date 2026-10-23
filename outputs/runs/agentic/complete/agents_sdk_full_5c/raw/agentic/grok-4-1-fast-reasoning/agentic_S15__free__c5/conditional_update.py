from database_client import get_mongo_collection
from typing import Dict, Any, Optional

def conditional_update(
    db_name: str,
    collection_name: str,
    doc_id: str,
    updates: Dict[str, Any],
    expected_version: Optional[int] = None
) -> bool:
    collection = get_mongo_collection(db_name, collection_name)
    filter_query = {"_id": doc_id}
    if expected_version is not None:
        filter_query["version"] = expected_version
    update_query = {"$set": updates, "$inc": {"version": 1}}
    result = collection.update_one(filter_query, update_query)
    return result.matched_count > 0