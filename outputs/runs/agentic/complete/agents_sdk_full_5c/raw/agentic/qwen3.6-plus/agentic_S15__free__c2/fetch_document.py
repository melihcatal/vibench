"""
Fetch a document by identifier from a MongoDB Atlas managed NoSQL document store.
Uses the official PyMongo SDK (pymongo) for MongoDB Atlas integration.
"""

from typing import Optional

from pymongo.collection import Collection

from database_client import get_collection
from database_models import (
    DocumentFetchRequest,
    DocumentResponse,
    normalize_document_result,
)


def fetch_document(
    collection_name: str,
    document_id: str,
    client=None,
) -> DocumentResponse:
    """
    Fetch a single document by its _id from MongoDB Atlas.

    Args:
        collection_name: Name of the MongoDB collection.
        document_id: The document's primary identifier.
        client: Optional pre-configured MongoClient instance.

    Returns:
        DocumentResponse containing the retrieved document or an error.
    """
    request = DocumentFetchRequest(
        collection_name=collection_name,
        document_id=document_id,
    )

    collection = get_collection(collection_name, client=client)

    try:
        raw_doc = collection.find_one({"_id": request.document_id})

        if raw_doc is None:
            return DocumentResponse(
                id=document_id,
                data={},
                metadata={},
                success=False,
                error="Document not found",
            )

        return normalize_document_result(raw_doc)
    except Exception as exc:
        return DocumentResponse(
            id=document_id,
            data={},
            metadata={},
            success=False,
            error=str(exc),
        )


if __name__ == "__main__":
    response = fetch_document(collection_name="documents", document_id="doc-001")
    print(response.to_dict())
