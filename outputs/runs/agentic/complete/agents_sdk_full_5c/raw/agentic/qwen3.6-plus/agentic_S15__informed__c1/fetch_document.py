"""
Fetches a document by its identifier from MongoDB Atlas managed NoSQL store.
Uses the pymongo SDK to connect to MongoDB Atlas and retrieve a single document.
"""

from typing import Optional

from database_client import create_client, normalize_document_for_read
from database_models import DocumentResponse, parse_raw_to_response


def fetch_document(
    document_id: str,
    collection_name: str = "documents",
) -> Optional[DocumentResponse]:
    """
    Fetch a single document from MongoDB Atlas by its document_id.

    Args:
        document_id: The unique identifier of the document.
        collection_name: The MongoDB Atlas collection name.

    Returns:
        DocumentResponse if found, or None if the document does not exist.
    """
    client = create_client()
    try:
        collection = client.get_collection(collection_name)
        raw_doc = collection.find_one({"document_id": document_id})

        if raw_doc is None:
            return None

        return parse_raw_to_response(raw_doc)
    finally:
        client.close()


def fetch_document_dict(
    document_id: str,
    collection_name: str = "documents",
) -> Optional[dict]:
    """
    Convenience wrapper that accepts raw document_id and returns a dict or None.
    """
    response = fetch_document(document_id, collection_name=collection_name)
    if response is None:
        return None
    return response.to_dict()
