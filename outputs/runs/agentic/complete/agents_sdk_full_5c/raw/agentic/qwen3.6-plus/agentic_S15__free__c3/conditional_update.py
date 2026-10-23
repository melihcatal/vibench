"""
conditional_update.py - Applies a conditional or version-aware update to one
stored document in MongoDB Atlas. Uses PyMongo's find_one_and_update with a
filter on the version field to ensure optimistic concurrency control.
"""

from typing import Any, Dict, Optional

from pymongo.errors import DuplicateKeyError

from database_client import build_atlas_client, AtlasClientHelper
from database_models import DocumentRequest, DocumentResponse, normalize_mongo_object_id


class ConditionalUpdateError(Exception):
    """Raised when a conditional update fails due to version mismatch or condition not met."""

    pass


def conditional_update(
    doc_id: str,
    collection_name: str,
    update_data: Dict[str, Any],
    current_version: Optional[int] = None,
    condition: Optional[Dict[str, Any]] = None,
    client: Optional[AtlasClientHelper] = None,
) -> DocumentResponse:
    """
    Apply a conditional or version-aware update to a document in MongoDB Atlas.

    Uses optimistic concurrency: if current_version is provided, the update
    only succeeds if the document's version field matches. Otherwise, an
    arbitrary condition filter can be supplied.

    Args:
        doc_id: The _id of the document to update.
        collection_name: MongoDB collection name.
        update_data: Fields to update (merged into the document's "data" sub-document).
        current_version: Expected version for optimistic concurrency.
        condition: Optional extra MongoDB query filter for conditional update.
        client: Optional pre-built AtlasClientHelper instance.

    Returns:
        DocumentResponse with the updated document.

    Raises:
        ConditionalUpdateError: If the version or condition does not match.
    """
    if client is None:
        client = build_atlas_client()

    collection = client.get_collection(collection_name)

    # Build the query filter: match _id and optionally the version
    query_filter: Dict[str, Any] = {"_id": doc_id}
    if current_version is not None:
        query_filter["version"] = current_version
    if condition:
        query_filter.update(condition)

    # Build the update: merge data into the "data" sub-document and bump version
    update_fields: Dict[str, Any] = {
        "$set": {
            **{f"data.{k}": v for k, v in update_data.items()},
            "version": (current_version + 1) if current_version is not None else 1,
        }
    }

    result = collection.find_one_and_update(
        query_filter,
        update_fields,
        return_document=True,
    )

    if result is None:
        raise ConditionalUpdateError(
            f"Conditional update failed for doc_id={doc_id}: "
            f"version mismatch or condition not satisfied."
        )

    result = normalize_mongo_object_id(result)
    return DocumentResponse.from_mongo_document(result)


if __name__ == "__main__":
    try:
        resp = conditional_update(
            doc_id="doc-001",
            collection_name="documents",
            update_data={"title": "Updated Title", "status": "active"},
            current_version=0,
        )
        print(resp.to_json())
    except ConditionalUpdateError as e:
        print(f"Update failed: {e}")
