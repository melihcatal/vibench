from __future__ import annotations

from typing import Any, Dict

from pymongo import ReplaceOne

from database_client import get_collection, normalize_identifier
from database_models import OperationResponse, UpsertRequest, ensure_primary_identifier, normalize_record


def upsert_document(request: UpsertRequest) -> OperationResponse:
    collection = get_collection()
    document = ensure_primary_identifier(normalize_identifier(request.document))
    identifier = document.get("_id", document.get("id"))
    if "_id" not in document:
        document["_id"] = identifier
    result = collection.replace_one({"_id": identifier}, document, upsert=True)
    stored = collection.find_one({"_id": identifier})
    return OperationResponse(
        ok=True,
        matched_count=result.matched_count,
        modified_count=result.modified_count,
        upserted_id=result.upserted_id,
        document=normalize_record(stored) if stored else document,
        message="document upserted",
    )
