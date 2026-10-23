"""Upsert a JSON document by its primary identifier in MongoDB Atlas.

Provider: MongoDB Atlas (pymongo)
Auth env: MONGODB_ATLAS_URI
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from database_client import get_collection
from database_models import DocumentRequest, DocumentResponse, normalize_upsert_payload


def upsert_document(
    doc_id: str,
    payload: Dict[str, Any],
    collection_name: Optional[str] = None,
) -> DocumentResponse:
    """Insert or replace a document in MongoDB Atlas identified by *doc_id*.

    Uses ``replace_one`` with ``upsert=True`` so the operation is idempotent.
    """
    collection = get_collection(collection_name=collection_name)
    request = normalize_upsert_payload(dict(payload), doc_id)
    mongo_doc = request.to_mongo_document()

    result = collection.replace_one(
        {"_id": doc_id},
        mongo_doc,
        upsert=True,
    )

    if result.upserted_id is not None:
        mongo_doc["_id"] = str(result.upserted_id)

    return DocumentResponse.from_mongo(mongo_doc)


def upsert_document_from_env(doc_id: str) -> DocumentResponse:
    """Upsert a document using payload read from the DOCUMENT_PAYLOAD env var."""
    import json
    raw = os.environ.get("DOCUMENT_PAYLOAD", "{}")
    payload = json.loads(raw)
    return upsert_document(doc_id, payload)


if __name__ == "__main__":
    resp = upsert_document_from_env("sample-doc-001")
    print(f"Upserted: found={resp.found}, id={resp.doc_id}, version={resp.version}")
