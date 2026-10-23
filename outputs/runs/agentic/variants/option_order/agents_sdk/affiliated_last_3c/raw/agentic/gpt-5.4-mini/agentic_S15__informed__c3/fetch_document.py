from __future__ import annotations

from database_client import get_collection
from database_models import FetchRequest, OperationResponse, normalize_record


def fetch_document(request: FetchRequest) -> OperationResponse:
    collection = get_collection()
    document = collection.find_one({"_id": request.identifier})
    return OperationResponse(
        ok=document is not None,
        document=normalize_record(document) if document else None,
        message="document found" if document else "document not found",
    )
