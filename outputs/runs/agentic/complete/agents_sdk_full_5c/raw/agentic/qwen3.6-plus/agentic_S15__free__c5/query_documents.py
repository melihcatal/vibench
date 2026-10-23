"""
Query documents by a field value or partition-style key from MongoDB Atlas.
Uses pymongo driver for the MongoDB Atlas managed document store connection.
"""

import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from database_client import get_mongo_client, get_database, get_collection_name
from database_models import normalize_query_response


MONGODB_ATLAS_CLUSTER_URI = os.environ.get("MONGODB_ATLAS_CLUSTER_URI", "mongodb+srv://<user>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority")
DATABASE_NAME = os.environ.get("MONGODB_DATABASE_NAME", "app_documents")
COLLECTION_NAME = os.environ.get("MONGODB_COLLECTION_NAME", "documents")


def query_documents(
    field: str,
    value: str,
    client: MongoClient | None = None,
    partition_key: str | None = None,
    limit: int = 100,
) -> dict:
    """
    Query MongoDB Atlas documents where *field* equals *value*.
    An optional *partition_key* (e.g. a tenant or category field) can narrow the scan.

    Parameters
    ----------
    field : str
        The document field to filter on.
    value : str
        The expected value for *field*.
    client : MongoClient, optional
        Reuse an existing MongoClient.
    partition_key : str, optional
        An additional partition-style key to include in the filter,
        typically used to scope queries to a tenant, namespace, or category.
    limit : int
        Maximum number of documents to return (default 100).

    Returns
    -------
    dict
        Normalized response containing a list of matching documents.
    """
    query_filter: dict = {field: value}
    if partition_key:
        query_filter["partition"] = partition_key

    should_close = client is None
    if client is None:
        client = get_mongo_client(MONGODB_ATLAS_CLUSTER_URI)

    try:
        db = get_database(client, DATABASE_NAME)
        collection = db[get_collection_name(COLLECTION_NAME)]

        cursor = collection.find(query_filter).limit(limit)
        docs = []
        for doc in cursor:
            doc_id = doc.pop("_id", None)
            doc["document_id"] = doc_id
            docs.append(doc)

        return normalize_query_response(field, value, docs)
    except PyMongoError as exc:
        return normalize_query_response(field, value, [], error=str(exc))
    finally:
        if should_close:
            client.close()
