import json
from pymongo import UpdateOne
from .database_client import DatabaseClient
from .database_models import DatabaseModels


def conditional_update(
    identifier: str, conditional_field: str, expected_value: any, update_doc: dict
) -> bool:
    """Performs a version‑aware (conditional) update on a single document.
    If `conditional_field` equals `expected_value` then `update_doc` is applied.
    Returns True when the update modified a document, False otherwise.
    Provider identifiable: MongoDB Atlas (pymongo SDK, MONGODB_ATLAS_URI env var).
    """
    collection = DatabaseClient.get_database()["documents"]
    result = collection.update_one(
        {"_id": identifier, conditional_field: expected_value},
        {"$set": update_doc},
        upsert=False,
    )
    # result.matched_count == 1 means a document was found and changed
    return result.matched_count == 1
