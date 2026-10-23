from __future__ import annotations

from typing import Any

from database_client import get_container, get_cosmos_client
from database_models import DocumentRecord, QueryRequest, QueryResponse


def query_documents(field_name: str, field_value: Any, partition_key: str | None = None, limit: int = 25) -> QueryResponse:
    client = get_cosmos_client()
    container = get_container(client)
    request = QueryRequest(field_name=field_name, field_value=field_value, partition_key=partition_key, limit=limit)

    if request.partition_key is not None:
        query = (
            f"SELECT TOP @limit * FROM c WHERE c.partition_key = @partition_key AND c.{request.field_name} = @field_value"
        )
        parameters = [
            {"name": "@limit", "value": request.limit},
            {"name": "@partition_key", "value": request.partition_key},
            {"name": "@field_value", "value": request.field_value},
        ]
        items = container.query_items(
            query=query,
            parameters=parameters,
            partition_key=request.partition_key,
        )
    else:
        query = f"SELECT TOP @limit * FROM c WHERE c.{request.field_name} = @field_value"
        parameters = [
            {"name": "@limit", "value": request.limit},
            {"name": "@field_value", "value": request.field_value},
        ]
        items = container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True,
        )

    records = [DocumentRecord.from_cosmos_item(item) for item in items]
    return QueryResponse(records=records, count=len(records))
