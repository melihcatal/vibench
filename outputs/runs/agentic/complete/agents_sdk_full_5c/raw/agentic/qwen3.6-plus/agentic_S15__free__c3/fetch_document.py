"""
fetch_document.py - Fetches a document by identifier from MongoDB Atlas.
Uses the PyMongo SDK to query a MongoDB Atlas managed collection by _id.
"""

from typing import Optional

from database_client import build_atlas_client, AtlasClientHelper
from database_models import DocumentResponse, normalize_mongo_object_id


def fetch_document(
    doc_id: str,
    collection_name: str,
    client: Optional[AtlasClientHelper] = None,
) -> DocumentResponse:
    """
    Fetch a single document from MongoDB Atlas by its _id.

    Args:
        doc_id: The unique identifier of the document.
        collection_name: Name of the MongoDB collection to query.
        client: Optional pre-built AtlasClientHelper instance.

    Returns:
        DocumentResponse with the found document data, or not_found response.
    """
    if client is None:
        client = build_atlas_client()

    collection = client.get_collection(collection_name)
    raw_doc = collection.find_one({"_id": doc_id})

    if raw_doc is None:
        return DocumentResponse.not_found(doc_id)

    raw_doc = normalize_mongo_object_id(raw_doc)
    return DocumentResponse.from_mongo_document(raw_doc)


if __name__ == "__main__":
    resp = fetch_document(doc_id="doc-001", collection_name="documents")
    print(resp.to_json())
