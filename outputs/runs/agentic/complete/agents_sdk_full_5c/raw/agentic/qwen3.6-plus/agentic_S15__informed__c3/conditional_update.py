"""
[SAME-SCENARIO] conditional_update.py
Applies a conditional or version-aware update to one stored document in MongoDB Atlas.
Provider: MongoDB Atlas via pymongo SDK.
Auth: MONGODB_ATLAS_URI
"""

from typing import Any, Dict, Optional

from database_client import get_mongo_client, get_collection, get_database_name, get_collection_name
from database_models import DocumentResponse


class ConditionalUpdateError(Exception):
    """Raised when the conditional update fails because the precondition was not met."""
    pass


def conditional_update(
    document_id: str,
    new_data: Dict[str, Any],
    expected_version: Optional[int] = None,
    database_name: str | None = None,
    collection_name: str | None = None,
) -> DocumentResponse:
    """
    Perform a version-aware (optimistic concurrency) update on a MongoDB Atlas document.
    The update only succeeds if the stored document's version matches expected_version.

    Args:
        document_id: The primary identifier of the document to update.
        new_data: The replacement data payload.
        expected_version: The version the document must currently have.
        database_name: Optional override for the target database name.
        collection_name: Optional override for the target collection name.

    Returns:
        DocumentResponse with the updated document.

    Raises:
        ConditionalUpdateError: If the version precondition is not satisfied.
    """
    client = get_mongo_client()
    try:
        db_name = database_name or get_database_name()
        col_name = collection_name or get_collection_name()
        collection = get_collection(client, db_name, col_name)

        query: Dict[str, Any] = {"_id": document_id}
        if expected_version is not None:
            query["version"] = expected_version

        update = {
            "$set": {
                "data": new_data,
                "version": (expected_version or 0) + 1,
            }
        }

        result = collection.update_one(query, update)

        if result.matched_count == 0:
            raise ConditionalUpdateError(
                f"Conditional update failed for document '{document_id}': "
                f"version mismatch or document not found."
            )

        updated_doc = collection.find_one({"_id": document_id})
        return DocumentResponse.from_mongo_doc(updated_doc)
    finally:
        client.close()


if __name__ == "__main__":
    try:
        updated = conditional_update("doc-001", {"title": "Updated Title"}, expected_version=1)
        print(f"Updated: {updated.to_dict()}")
    except ConditionalUpdateError as exc:
        print(f"Error: {exc}")
