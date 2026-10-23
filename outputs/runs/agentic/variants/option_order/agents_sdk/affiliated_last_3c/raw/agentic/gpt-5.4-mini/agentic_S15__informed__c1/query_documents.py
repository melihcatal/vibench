from __future__ import annotations

from typing import Any, List

from database_client import get_collection, serialize_snapshot
from database_models import QueryRequest, QueryResponse


def query_documents(collection: str, field_name: str, field_value: Any, limit: int = 50) -> QueryResponse:
    request = QueryRequest(collection=collection, field_name=field_name, field_value=field_value, limit=limit)
    query = get_collection(request.collection).where(request.field_name, "==", request.field_value).limit(request.limit)
    items: List[dict] = [serialize_snapshot(snapshot) for snapshot in query.stream()]
    return QueryResponse(items=items, count=len(items))
