"""
Upsert a JSON document into MongoDB Atlas by its primary identifier.
Uses pymongo driver connecting to MongoDB Atlas managed cluster.
"""

import os
from datetime import datetime, timezone

from pymongo import MongoClient, UpdateOne
from pymongo.errors import PyMongoError

from database_client import get_mongo_client, get_database, get_collection_name
from database_models import build_upsert_payload, normalize_upsert_response


MONGODB_ATLAS_CLUSTER_URI = os.environ.get("MONGODB_ATLAS_CLUSTER_URI", "mongodb+srv://<user>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority")
DATABASE_NAME = os.environ.get("MONGODB_DATABASE_NAME", "app_documents")
COLLECTION_NAME = os.environ.get("MONGODB_COLLECTION_NAME", "documents")


def upsert_document(
    document_id: str,
    data: dict,
    client: MongoClient | None = None,
) -> dict:
    """
    Upsert a document identified by *document_id* into the configured MongoDB Atlas collection.
    If the document exists, it is replaced with the new payload; otherwise, it is inserted.

    Parameters
    ----------
    document_id : str
        The primary identifier for the document (stored as the MongoDB ``_id`` field).
    data : dict
        The JSON-serializable payload to store.
    client : MongoClient, optional
        Reuse an existing MongoClient.  One is created from environment
        variables when ``None``.

    Returns
    -------
    dict
        Normalized response indicating success, the document id, and whether it was new.
    """
    payload = build_upsert_payload(document_id, data)
    payload["updated_at"] = datetime.now(timezone.utc)

    should_close = client is None
    if client is None:
        client = get_mongo_client(MONGODB_ATLAS_CLUSTER_URI)

    try:
        db = get_database(client, DATABASE_NAME)
        collection = db[get_collection_name(COLLECTION_NAME)]

        result = collection.update_one(
            {"_id": document_id},
            {"$set": payload},
            upsert=True,
        )

        was_new = result.upserted_id is not None
        return normalize_upsert_response(document_id, was_new, result.modified_count)
    except PyMongoError as exc:
        return normalize_upsert_response(document_id, False, 0, error=str(exc))
    finally:
        if should_close:
            client.close()
