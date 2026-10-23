from __future__ import annotations

from typing import Any, Dict, List

from database_client import get_container
from database_models import QueryRequest, normalize_documents



def query_documents(field_name: str, field_value: Any, partition_key: str | None = None, limit: int = 100) -> List[Dict[str, Any]]:
    container = get_container()
    request = QueryRequest(
        field_name=field_name,
        field_value=field_value,
        partition_key=partition_key,
        limit=limit,
    )
    query = f"SELECT * FROM c WHERE c[{request.field_name!r}] = @field_value"
    parameters = [{"name": "@field_value", "value": request.field_value}]
    if request.partition_key is not None:
        query += " AND c.partitionKey = @partition_key"
        parameters.append({"name": "@partition_key", "value": request.partition_key})
    query += " OFFSET 0 LIMIT @limit"
    parameters.append({"name": "@limit", "value": request.limit})
    items = container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=request.partition_key is None,
    )
    return normalize_documents(items)
