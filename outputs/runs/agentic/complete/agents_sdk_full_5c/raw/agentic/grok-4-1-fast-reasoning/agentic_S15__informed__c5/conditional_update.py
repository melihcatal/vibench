from database_client import get_collection
from typing import Dict, Any, Optional

def conditional_update(document_id: str, updates: Dict[str, Any], expected_version: Optional[int] = None) -> bool:
    coll = get_collection()
    query_filter = {"_id": document_id}
    if expected_version is not None:
        query_filter["version"] = expected_version
    update_ops = {"$set": updates, "$inc": {"version": 1}}
    result = coll.update_one(query_filter, update_ops)
    return result.modified_count > 0
