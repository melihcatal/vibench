from database_client import get_db_client
from bson import ObjectId
from pymongo.results import UpdateResult


def conditional_update(
    document_id: str, update_data: dict, expected_version: int
) -> UpdateResult:
    """
    Applies a conditional update to a document in MongoDB Atlas
    based on the document's version.
    """
    client = get_db_client()
    query = {"_id": ObjectId(document_id), "_version": expected_version}

    update = {"$set": update_data, "$inc": {"_version": 1}}

    result = client.update_one(query, update)
    return result
