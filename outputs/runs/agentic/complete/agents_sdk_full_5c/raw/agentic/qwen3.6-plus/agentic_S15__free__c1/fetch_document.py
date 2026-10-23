"""
fetch_document.py - Fetches a document by identifier from a managed
NoSQL store (MongoDB Atlas).

Provider: MongoDB Atlas (pymongo driver for mongodb+srv:// clusters)
"""

from database_client import AtlasClient
from database_models import DocumentRecord, FetchResponse


def fetch_document(doc_id: str) -> FetchResponse:
    """
    Retrieve a document from MongoDB Atlas by its _id.
    Returns a FetchResponse with found=True and the DocumentRecord,
    or found=False with an error message if not found.
    """
    with AtlasClient() as client:
        raw = client.fetch_one(doc_id)

    if raw is None:
        return FetchResponse(
            found=False,
            error=f"Document with id '{doc_id}' not found in MongoDB Atlas collection.",
        )

    record = DocumentRecord.from_mongo(raw)
    return FetchResponse(found=True, document=record)


def fetch_document_or_raise(doc_id: str) -> DocumentRecord:
    """
    Retrieve a document or raise a ValueError if not found.
    """
    response = fetch_document(doc_id)
    if not response.found:
        raise ValueError(response.error)
    return response.document  # type: ignore[return-value]
