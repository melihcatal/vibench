"""
Applies a conditional or version-aware update to one document in MongoDB Atlas.

Provider: MongoDB Atlas
SDK: pymongo
Auth: MONGODB_ATLAS_URI
Interface: SDK (pymongo)
"""

from typing import Any, Dict, Optional

from database_client import get_collection
from database_models import (
    format_conditional_query,
    build_update_payload,
    normalize_document,
    build_response,
)


def conditional_update(
    document_id: str,
    updates: Dict[str, Any],
    condition_field: str = "_version",
    condition_value: Optional[Any] = None,
    collection_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Apply a conditional, version-aware update to a MongoDB Atlas document.

    Uses an optimistic-concurrency pattern: the update only proceeds if the
    document's version field (or specified condition field) matches the
    expected value. On success, the version is incremented.

    Args:
        document_id: The _id of the document to update.
        updates: Dictionary of fields to update.
        condition_field: The field used for the conditional check (default: _version).
        condition_value: The expected value for the condition field.
        collection_name: Optional collection override.

    Returns:
        A response dict with success status and the updated document.
    """
    collection = get_collection(collection_name)

    # Auto-increment version on update
    update_payload = build_update_payload(updates, document_id=document_id)
    if condition_field == "_version":
        update_payload["$inc"] = {"_version": 1}

    query = format_conditional_query(document_id, condition_field, condition_value)

    result = collection.update_one(query, update_payload)

    if result.matched_count == 0:
        return build_response(
            success=False,
            message=(
                f"Conditional update failed: no document matched the "
                f"condition {condition_field}={condition_value} in MongoDB Atlas."
            ),
            error="CONDITION_NOT_MET",
        )

    # Fetch the updated document for the response
    updated_doc = collection.find_one({"_id": document_id})
    normalized = normalize_document(updated_doc) if updated_doc else None

    return build_response(
        success=True,
        data={
            "document_id": document_id,
            "modified_count": result.modified_count,
            "document": normalized,
        },
        message=f"Conditional update applied successfully in MongoDB Atlas.",
    )
