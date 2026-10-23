from __future__ import annotations

from typing import Any, Dict, List

from database_client import get_container
from database_models import OperationResult, QueryRequest, normalize_documents


def query_documents(field_name: str | None = None, field_value: Any = None, partition_key: str | None = None, max_items: int = 50) -> OperationResult:
    container = get_container()
    request = QueryRequest(field_name=field_name, field_value=field_value, partition_key=partition_key, max_items=max_items)

    if request.partition_key and not request.field_name:
        query = "SELECT * FROM c WHERE c.partitionKey = @partitionKey"
        parameters: List[Dict[str, Any]] = [{"name": "@partitionKey", "value": request.partition_key}]
    elif request.field_name:
        query = f"SELECT * FROM c WHERE c[{repr(request.field_name)}] = @fieldValue"
        parameters = [{"name": "@fieldValue", "value": request.field_value}]
        if request.partition_key:
            query += " AND c.partitionKey = @partitionKey"
            parameters.append({"name": "@partitionKey", "value": request.partition_key})
    else:
        query = "SELECT * FROM c"
        parameters = []

    items = list(
        container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True,
            max_item_count=request.max_items,
        )
    )
    return OperationResult(
        ok=True,
        items=normalize_documents(items),
        status_code=200,
        message="Queried Azure Cosmos DB",
    )
