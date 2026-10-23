from __future__ import annotations

from typing import Any

from database_client import get_collection
from database_models import DocumentRequest, DocumentResponse
from pymongo.collection import Collection


def upsert_document(
    document_id: str,
    data: dict[str, Any],
    partition_key: str | None = None,
    version: int | None = None,
    collection: Collection | None = None,
) -> DocumentResponse:
    if collection is None:
        collection = get_collection()

    request = DocumentRequest(
        document_id=document_id,
        data=data,
        partition_key=partition_key,
        version=version,
    )

    payload = request.to_mongo_payload()

    collection.replace_one(
        {"_id": document_id},
        payload,
        upsert=True,
    )

    result_doc = collection.find_one({"_id": document_id})
    return DocumentResponse.from_mongo(result_doc)
