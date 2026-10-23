from typing import Dict, Any
from pymongo import ReturnDocument
from database_client import get_mongodb_client, get_database, get_collection


def conditional_update(
    doc_id: str, expected_version: int, updates: Dict[str, Any]
) -> bool:
    client = get_mongodb_client()
    db = get_database(client)
    coll = get_collection(db)
    result = coll.find_one_and_update(
        {"_id": doc_id, "version": expected_version},
        {"$set": updates, "$inc": {"version": 1}},
        return_document=ReturnDocument.AFTER,
        upsert=False,
    )
    client.close()
    return result is not None
