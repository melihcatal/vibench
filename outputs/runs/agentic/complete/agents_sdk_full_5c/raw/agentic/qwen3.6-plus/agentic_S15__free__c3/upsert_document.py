"""
upsert_document.py - Upserts a JSON document by its primary identifier in MongoDB Atlas.
Uses the PyMongo SDK to connect to a MongoDB Atlas cluster and performs an
upsert via update_one with upsert=True on the specified collection.
"""

from typing import Any, Dict, Optional

from database_client import build_atlas_client, AtlasClientHelper
from database_models import DocumentRequest, DocumentResponse, normalize_mongo_object_id


def upsert_document(
    doc_id: str,
    collection_name: str,
    data: Dict[str, Any],
    client: Optional[AtlasClientHelper] = None,
) -> DocumentResponse:
    """
    Upsert a JSON document identified by doc_id into the given MongoDB Atlas collection.

    Args:
        doc_id: The unique document identifier (used as _id).
        collection_name: Name of the MongoDB collection.
        data: The JSON/document payload to store.
        client: Optional pre-built AtlasClientHelper instance.

    Returns:
        DocumentResponse representing the upserted document state.
    """
    if client is None:
        client = build_atlas_client()

    collection = client.get_collection(collection_name)
    request = DocumentRequest(doc_id=doc_id, data=data)
    mongo_doc = request.to_mongo_document()

    result = collection.update_one(
        {"_id": doc_id},
        {"$set": mongo_doc},
        upsert=True,
    )

    # Fetch the final document state after upsert
    saved_doc = collection.find_one({"_id": doc_id})
    if saved_doc is None:
        return DocumentResponse.not_found(doc_id)

    saved_doc = normalize_mongo_object_id(saved_doc)
    response = DocumentResponse.from_mongo_document(saved_doc)

    return response


if __name__ == "__main__":
    import sys

    sample_data = {
        "title": "Sample Document",
        "body": "This is a test document stored in MongoDB Atlas.",
        "tags": ["example", "test"],
        "metadata": {"source": "upsert_document.py"},
    }
    resp = upsert_document(
        doc_id="doc-001",
        collection_name="documents",
        data=sample_data,
    )
    print(resp.to_json())
