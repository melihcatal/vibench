"""
Fetch a document by identifier from MongoDB Atlas managed NoSQL document store.
Uses pymongo driver for the MongoDB Atlas connection.
"""

import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from database_client import get_mongo_client, get_database, get_collection_name
from database_models import normalize_fetch_response


MONGODB_ATLAS_CLUSTER_URI = os.environ.get("MONGODB_ATLAS_CLUSTER_URI", "mongodb+srv://<user>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority")
DATABASE_NAME = os.environ.get("MONGODB_DATABASE_NAME", "app_documents")
COLLECTION_NAME = os.environ.get("MONGODB_COLLECTION_NAME", "documents")


def fetch_document(
    document_id: str,
    client: MongoClient | None = None,
    projection: dict | None = None,
) -> dict:
    """
    Retrieve a single document from MongoDB Atlas by its primary identifier.

    Parameters
    ----------
    document_id : str
        The ``_id`` value of the document to fetch.
    client : MongoClient, optional
        Reuse an existing MongoClient.  Created from env vars when ``None``.
    projection : dict, optional
        MongoDB projection spec to limit returned fields.

    Returns
    -------
    dict
        Normalized response with the document data or ``None`` when not found.
    """
    should_close = client is None
    if client is None:
        client = get_mongo_client(MONGODB_ATLAS_CLUSTER_URI)

    try:
        db = get_database(client, DATABASE_NAME)
        collection = db[get_collection_name(COLLECTION_NAME)]

        doc = collection.find_one({"_id": document_id}, projection=projection)

        if doc is None:
            return normalize_fetch_response(document_id, found=False, data=None)

        doc.pop("_id", None)
        return normalize_fetch_response(document_id, found=True, data=doc)
    except PyMongoError as exc:
        return normalize_fetch_response(document_id, found=False, data=None, error=str(exc))
    finally:
        if should_close:
            client.close()
