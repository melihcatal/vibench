from database_client import coll

def conditional_update(doc_id: str, updates: dict, expected_version: Optional[int] = None) -> bool:
    filter_query = {"_id": doc_id}
    if expected_version is not None:
        filter_query["version"] = expected_version
    result = coll.update_one(filter_query, {"$set": updates})
    return result.modified_count > 0