from __future__ import annotations

from typing import Any, Dict, List, Optional

from database_client import get_container
from database_models import OperationResult, QueryRequest, normalize_documents


def query_documents(field_name: str, field_value: Any, partition_key: Optional[str] = None, limit: int = 50) -> OperationResult:
    container = get_container()
    request = QueryRequest(field_name=field_name, field_value=field_value, partition_key=partition_key, limit=limit)

    query = f"SELECT TOP {int(request.limit)} * FROM c WHERE c[{repr(request.field_name)}] = @field_value"
    parameters: List[Dict[str, Any]] = [{"name": "@field_value", "value": request.field_value}]
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
    return OperationResult(
        success=True,
        documents=normalize_documents(items),
        status_message="Queried documents from Azure Cosmos DB",
    )
