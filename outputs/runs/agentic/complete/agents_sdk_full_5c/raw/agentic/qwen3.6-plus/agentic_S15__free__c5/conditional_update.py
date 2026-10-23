"""
Apply a conditional / version-aware update to a single document in MongoDB Atlas.
Uses pymongo's optimistic concurrency pattern via an etag/version field.
"""

import os
from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from database_client import get_mongo_client, get_database, get_collection_name
from database_models import normalize_conditional_update_response


MONGODB_ATLAS_CLUSTER_URI = os.environ.get("MONGODB_ATLAS_CLUSTER_URI", "mongodb+srv://<user>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority")
DATABASE_NAME = os.environ.get("MONGODB_DATABASE_NAME", "app_documents")
COLLECTION_NAME = os.environ.get("MONGODB_COLLECTION_NAME", "documents")


def conditional_update(
    document_id: str,
    updates: dict,
    expected_version: int,
    client: MongoClient | None = None,
) -> dict:
    """
    Conditionally update a document in MongoDB Atlas only if its current
    ``version`` field matches *expected_version*.  On success, the version is
    incremented atomically.

    Parameters
    ----------
    document_id : str
        The primary ``_id`` of the document.
    updates : dict
        Field-level updates to apply (will be set via ``$set``).
    expected_version : int
        The version the caller believes the document currently has.
    client : MongoClient, optional
        Reuse an existing MongoClient.

    Returns
    -------
    dict
        Normalized response indicating success or a version-mismatch / error.
    """
    should_close = client is None
    if client is None:
        client = get_mongo_client(MONGODB_ATLAS_CLUSTER_URI)

    try:
        db = get_database(client, DATABASE_NAME)
        collection = db[get_collection_name(COLLECTION_NAME)]

        new_version = expected_version + 1
        update_doc = {"$set": {**updates, "version": new_version, "updated_at": datetime.now(timezone.utc)}}

        result = collection.update_one(
            {"_id": document_id, "version": expected_version},
            update_doc,
        )

        if result.matched_count == 0:
            current = collection.find_one({"_id": document_id})
            current_version = current.get("version") if current else None
            return normalize_conditional_update_response(
                document_id, success=False, reason="version_mismatch",
                current_version=current_version, expected_version=expected_version,
            )

        return normalize_conditional_update_response(
            document_id, success=True, new_version=new_version, modified_count=result.modified_count,
        )
    except PyMongoError as exc:
        return normalize_conditional_update_response(
            document_id, success=False, reason="error", error=str(exc),
        )
    finally:
        if should_close:
            client.close()
