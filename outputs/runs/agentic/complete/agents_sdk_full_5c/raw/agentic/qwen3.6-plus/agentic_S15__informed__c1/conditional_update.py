"""
Applies a conditional or version-aware update to one stored document in MongoDB Atlas.
Uses the pymongo SDK to connect to MongoDB Atlas and perform a conditional update
with a document version check to prevent lost updates.
"""

from typing import Any, Dict, Optional

from database_client import create_client, normalize_document_for_write
from database_models import DocumentRequest, DocumentResponse, parse_raw_to_response


def conditional_update(
    document_id: str,
    update_data: Dict[str, Any],
    expected_version: Optional[int] = None,
    collection_name: str = "documents",
) -> Optional[DocumentResponse]:
    """
    Apply a conditional update to a document in MongoDB Atlas.

    If expected_version is provided, the update only succeeds when the stored
    document's _version matches expected_version. On success, the version is
    incremented automatically.

    Args:
        document_id: The unique identifier of the document to update.
        update_data: Dictionary of fields to update.
        expected_version: If set, the document must have this _version.
        collection_name: The MongoDB Atlas collection name.

    Returns:
        DocumentResponse with the updated document, or None if no match.
    """
    client = create_client()
    try:
        collection = client.get_collection(collection_name)

        match_filter: Dict[str, Any] = {"document_id": document_id}

        if expected_version is not None:
            match_filter["_version"] = expected_version

        set_fields = {k: v for k, v in update_data.items() if v is not None}
        if not set_fields:
            raise ValueError("No valid fields provided for update")

        update_payload = {
            "$set": set_fields,
            "$inc": {"_version": 1},
        }

        result = collection.update_one(match_filter, update_payload)

        if result.matched_count == 0:
            return None

        raw_doc = collection.find_one({"document_id": document_id})
        if raw_doc is None:
            raise RuntimeError("Updated document could not be retrieved")

        return parse_raw_to_response(raw_doc)
    finally:
        client.close()


def conditional_update_dict(
    document_id: str,
    update_data: Dict[str, Any],
    expected_version: Optional[int] = None,
    collection_name: str = "documents",
) -> Optional[Dict[str, Any]]:
    """
    Convenience wrapper returning a raw dict response or None.
    """
    response = conditional_update(
        document_id=document_id,
        update_data=update_data,
        expected_version=expected_version,
        collection_name=collection_name,
    )
    if response is None:
        return None
    return response.to_dict()
