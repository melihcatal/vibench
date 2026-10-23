"""
Upserts a JSON document by its primary identifier into MongoDB Atlas.
Uses the pymongo SDK to connect to MongoDB Atlas and perform an upsert
operation via replace_one with upsert=True.
"""

from typing import Any, Dict

from database_client import create_client, normalize_document_for_write
from database_models import DocumentRequest, DocumentResponse, parse_raw_to_response


def upsert_document(
    document_request: DocumentRequest,
    collection_name: str = "documents",
) -> DocumentResponse:
    """
    Upsert a document into MongoDB Atlas by its document_id.

    If the document exists, it is fully replaced. If it does not exist,
    a new document is inserted with the provided data.

    Args:
        document_request: The DocumentRequest containing document_id and data.
        collection_name: The MongoDB Atlas collection name.

    Returns:
        DocumentResponse representing the upserted document.
    """
    client = create_client()
    try:
        collection = client.get_collection(collection_name)
        payload = normalize_document_for_write(document_request.to_payload())

        result = collection.replace_one(
            {"document_id": document_request.document_id},
            payload,
            upsert=True,
        )

        # Fetch the document back to return a full response
        raw_doc = collection.find_one({"document_id": document_request.document_id})
        if raw_doc is None:
            raise RuntimeError("Failed to retrieve upserted document")

        return parse_raw_to_response(raw_doc)
    finally:
        client.close()


def upsert_document_dict(
    document_id: str,
    data: Dict[str, Any],
    collection_name: str = "documents",
) -> Dict[str, Any]:
    """
    Convenience wrapper that accepts raw dict input and returns a dict response.
    """
    request = DocumentRequest(document_id=document_id, data=data)
    response = upsert_document(request, collection_name=collection_name)
    return response.to_dict()
