from __future__ import annotations

from typing import Any, Dict, List, Optional

from database_client import CosmosDocumentStore
from database_models import QueryRequest, normalize_documents



def query_documents(field_name: str, field_value: Any, partition_key: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    request = QueryRequest(
        field_name=field_name,
        field_value=field_value,
        partition_key=partition_key,
        limit=limit,
    )
    container = CosmosDocumentStore().get_container()
    query = f"SELECT TOP {request.limit} * FROM c WHERE c[{repr(request.field_name)}] = @field_value"
    parameters = [{"name": "@field_value", "value": request.field_value}]
    if request.partition_key is not None:
        query += " AND c.partitionKey = @partition_key"
        parameters.append({"name": "@partition_key", "value": request.partition_key})
    items = list(
        container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=request.partition_key is None,
        )
    )
    return normalize_documents(items)
