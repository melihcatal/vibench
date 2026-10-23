"""Apply a conditional or version-aware update to one document in MongoDB Atlas.

Provider: MongoDB Atlas (pymongo)
Auth env: MONGODB_ATLAS_URI
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from database_client import get_collection
from database_models import DocumentResponse


def conditional_update(
    doc_id: str,
    updates: Dict[str, Any],
    expected_version: Optional[int] = None,
    collection_name: Optional[str] = None,
) -> DocumentResponse:
    """Update a document only if its current version matches *expected_version*.

    This provides optimistic concurrency control on MongoDB Atlas documents.
    The ``$set`` operator applies the updates and increments the version atomically.
    """
    collection = get_collection(collection_name=collection_name)

    filter_doc: Dict[str, Any] = {"_id": doc_id}
    if expected_version is not None:
        filter_doc["version"] = expected_version

    update_ops = {
        "$set": updates,
        "$inc": {"version": 1},
    }

    result = collection.update_one(filter_doc, update_ops)

    if result.matched_count == 0:
        # Document not found or version mismatch
        existing = collection.find_one({"_id": doc_id})
        return DocumentResponse.from_mongo(existing)

    updated_doc = collection.find_one({"_id": doc_id})
    return DocumentResponse.from_mongo(updated_doc)


if __name__ == "__main__":
    resp = conditional_update(
        "sample-doc-001",
        {"status": "archived"},
        expected_version=1,
    )
    if resp.found:
        print(f"Updated: id={resp.doc_id}, new version={resp.version}")
    else:
        print("Update failed: document not found or version mismatch")
