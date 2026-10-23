from __future__ import annotations

from database_client import get_collection
from database_models import DocumentResponse
from pymongo.collection import Collection


def fetch_document(
    document_id: str,
    collection: Collection | None = None,
) -> DocumentResponse:
    if collection is None:
        collection = get_collection()

    doc = collection.find_one({"_id": document_id})
    return DocumentResponse.from_mongo(doc)
