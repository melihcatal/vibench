from __future__ import annotations

from typing import Any, Dict, List, Optional

from database_client import get_container
from database_models import DocumentQueryRequest, normalize_document


def query_documents(
    field_name: str,
    field_value: Any,
    partition_key: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    request = DocumentQueryRequest(
        field_name=field_name,
        field_value=field_value,
        partition_key=partition_key,
        limit=limit,
    )
    container = get_container()
    query = f"SELECT * FROM c WHERE c.{request.field_name} = @value"
    parameters = [{"name": "@value", "value": request.field_value}]
    items = container.query_items(
        query=query,
        parameters=parameters,
        partition_key=request.partition_key,
        enable_cross_partition_query=request.partition_key is None,
        max_item_count=request.limit,
    )
    results: List[Dict[str, Any]] = []
    for item in items:
        results.append(normalize_document(item))
        if len(results) >= request.limit:
            break
    return results
