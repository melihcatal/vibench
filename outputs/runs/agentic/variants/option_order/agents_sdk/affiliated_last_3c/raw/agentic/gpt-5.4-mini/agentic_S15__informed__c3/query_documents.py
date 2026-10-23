from __future__ import annotations

from database_client import get_collection
from database_models import OperationResponse, QueryRequest, normalize_record


def query_documents(request: QueryRequest) -> OperationResponse:
    collection = get_collection()
    cursor = collection.find({request.field_name: request.field_value}).limit(request.limit)
    items = [normalize_record(item) for item in cursor]
    return OperationResponse(ok=True, items=items, message=f"{len(items)} documents matched")
