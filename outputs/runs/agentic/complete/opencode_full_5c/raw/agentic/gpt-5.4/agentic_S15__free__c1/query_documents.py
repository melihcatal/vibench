from __future__ import annotations

from typing import Any

from database_client import get_container, extract_cosmos_headers
from database_models import OperationResult, QueryRequest


def query_documents(
    field_name: str, field_value: Any, partition_key: str | None = None, limit: int = 50
) -> OperationResult:
    request = QueryRequest(
        field_name=field_name,
        field_value=field_value,
        partition_key=partition_key,
        limit=limit,
    ).normalized()
    container = get_container()
    query = f"SELECT TOP {request.limit} * FROM c WHERE c[{repr(request.field_name)}] = @field_value"
    parameters = [{"name": "@field_value", "value": request.field_value}]
    if request.partition_key is not None:
        query += " AND c.partition_key = @partition_key"
        parameters.append({"name": "@partition_key", "value": request.partition_key})
    items = list(
        container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=request.partition_key is None,
        )
    )
    headers = extract_cosmos_headers(container.client_connection.last_response_headers)
    return OperationResult(
        provider="azure_cosmos_db",
        success=True,
        documents=items,
        request_charge=headers["request_charge"],
    )
