"""
Upsert a JSON document by its primary identifier into a MongoDB Atlas managed NoSQL document store.
Uses the official PyMongo SDK (pymongo) for MongoDB Atlas integration.
"""

from typing import Dict, Any, Optional

from pymongo.collection import Collection
from pymongo.results import UpdateResult

from database_client import get_collection
from database_models import (
    DocumentUpsertRequest,
    DocumentResponse,
    build_upsert_response,
)


def upsert_document(
    collection_name: str,
    document_id: str,
    document: Dict[str, Any],
    version: Optional[int] = None,
    client=None,
) -> DocumentResponse:
    """
    Upsert (insert or replace) a document in the specified MongoDB Atlas collection.

    Args:
        collection_name: Name of the MongoDB collection.
        document_id: Primary identifier for the document.
        document: JSON-compatible dict representing the document body.
        version: Optional version number for optimistic concurrency tracking.
        client: Optional pre-configured MongoClient instance.

    Returns:
        DocumentResponse containing the upserted document or error info.
    """
    request = DocumentUpsertRequest(
        collection_name=collection_name,
        document_id=document_id,
        document=document,
        version=version,
    )

    collection = get_collection(collection_name, client=client)
    payload = request.to_mongo_payload()

    try:
        result: UpdateResult = collection.replace_one(
            {"_id": document_id},
            payload,
            upsert=True,
        )

        if result.upserted_id is not None:
            payload["_id"] = result.upserted_id

        return build_upsert_response(
            raw_doc=payload,
            success=True,
        )
    except Exception as exc:
        return build_upsert_response(
            raw_doc={"_id": document_id, **document},
            success=False,
            error=str(exc),
        )


if __name__ == "__main__":
    sample_doc = {
        "title": "Integration Test Record",
        "category": "sample",
        "tags": ["test", "upsert"],
        "content": {"body": "This is a test document for MongoDB Atlas upsert."},
    }
    response = upsert_document(
        collection_name="documents",
        document_id="doc-001",
        document=sample_doc,
    )
    print(response.to_dict())
