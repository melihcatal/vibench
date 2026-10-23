import os
from typing import Any
from database_client import get_mongo_client, get_database, get_collection
from database_models import normalize_document


def conditional_update(
    collection_name: str,
    document_id: str,
    updates: dict,
    expected_version: int,
    id_field: str = "_id",
    version_field: str = "version",
) -> dict:
    """
    Applies a conditional or version-aware update to one stored document in a MongoDB collection.
    The update only proceeds if the document's current version matches `expected_version`.
    If the update is successful, the version field in the document is incremented.
    """
    client = get_mongo_client()
    database = get_database(client)
    collection = get_collection(database, collection_name)

    # Prepare the update operation
    update_operation = {"$set": updates, "$inc": {version_field: 1}}

    # Define the filter to match the document by ID and expected version
    filter_query = {id_field: document_id, version_field: expected_version}

    result = collection.update_one(filter_query, update_operation)
    client.close()

    return {
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
        "acknowledged": result.acknowledged,
    }
