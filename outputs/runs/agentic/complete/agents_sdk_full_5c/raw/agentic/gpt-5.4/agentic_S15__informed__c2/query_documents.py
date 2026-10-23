from __future__ import annotations

from typing import Any, Dict, List, Optional

from database_client import get_collection
from database_models import QueryRequest, normalize_documents



def query_documents(field_name: str, field_value: Any, limit: int = 25, partition_key: Optional[str] = None) -> List[Dict[str, Any]]:
    collection = get_collection()
    request = QueryRequest(field_name=field_name, field_value=field_value, limit=limit)
    query: Dict[str, Any] = {request.field_name: request.field_value}
    if partition_key is not None:
        query["partition_key"] = partition_key
    cursor = collection.find(query).limit(request.limit)
    return normalize_documents(cursor)
