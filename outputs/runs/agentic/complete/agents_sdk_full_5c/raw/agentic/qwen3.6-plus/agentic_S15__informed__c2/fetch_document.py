"""Fetch a document by identifier from MongoDB Atlas.

Provider: MongoDB Atlas (pymongo)
Auth env: MONGODB_ATLAS_URI
"""

from __future__ import annotations

from typing import Optional

from database_client import get_collection
from database_models import DocumentResponse


def fetch_document(
    doc_id: str,
    collection_name: Optional[str] = None,
) -> DocumentResponse:
    """Retrieve a single document from MongoDB Atlas by its ``_id``."""
    collection = get_collection(collection_name=collection_name)
    doc = collection.find_one({"_id": doc_id})
    return DocumentResponse.from_mongo(doc)


if __name__ == "__main__":
    resp = fetch_document("sample-doc-001")
    if resp.found:
        print(f"Found document {resp.doc_id} (version={resp.version}): {resp.data}")
    else:
        print(f"Document not found")
