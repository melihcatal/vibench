from pymongo import ReturnDocument
from database_client import get_collection
from database_models import (
    DocumentUpsertRequest,
    DocumentResponse,
    build_upsert_payload,
    normalize_document,
)


def upsert_document(request: DocumentUpsertRequest) -> DocumentResponse:
    collection = get_collection()
    payload = build_upsert_payload(request)

    existing = collection.find_one({"document_id": request.document_id})
    current_version = existing.get("version", 0) if existing else 0
    payload["version"] = current_version + 1

    if existing and "created_at" in existing:
        payload["created_at"] = existing["created_at"]

    filter_criteria = {"document_id": request.document_id}
    if request.partition_key:
        filter_criteria["partition_key"] = request.partition_key

    result = collection.find_one_and_update(
        filter_criteria,
        {"$set": payload},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )

    return normalize_document(result)
