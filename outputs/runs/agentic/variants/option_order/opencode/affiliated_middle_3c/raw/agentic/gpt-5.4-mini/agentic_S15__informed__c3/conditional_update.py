from database_client import get_collection


def conditional_update(identifier, expected_version, updates):
    collection = get_collection()
    result = collection.update_one(
        {"_id": identifier, "version": expected_version},
        {"$set": updates, "$inc": {"version": 1}},
    )
    return {"matched": result.matched_count, "modified": result.modified_count}
