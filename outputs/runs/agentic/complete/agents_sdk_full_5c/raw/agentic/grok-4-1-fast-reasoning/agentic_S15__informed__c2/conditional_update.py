from database_client import get_collection
from pymongo import ReturnDocument

def conditional_update(doc_id: str, updates: dict, expected_version: int = None) -> dict | None:
    coll = get_collection()
    query = {'_id': doc_id}
    if expected_version is not None:
        query['version'] = expected_version
    result = coll.find_one_and_update(
        query,
        {'$set': updates, '$inc': {'version': 1}},
        return_document=ReturnDocument.AFTER
    )
    return result