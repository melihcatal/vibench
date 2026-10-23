from __future__ import annotations

from typing import Any

from database_client import get_container
from database_models import QueryRequest, build_document_record


def query_documents(
    field_name: str, field_value: Any, partition_key: str | None = None, limit: int = 25
) -> list[dict[str, Any]]:
    container = get_container()
    request = QueryRequest(
        field_name=field_name,
        field_value=field_value,
        partition_key=partition_key,
        limit=limit,
    )
    query = f"SELECT TOP {request.limit} * FROM c WHERE c.{request.field_name} = @fieldValue"
    parameters: list[dict[str, Any]] = [
        {"name": "@fieldValue", "value": request.field_value}
    ]
    if request.partition_key is not None:
        query += " AND c.partitionKey = @partitionKey"
        parameters.append({"name": "@partitionKey", "value": request.partition_key})
    results = container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=request.partition_key is None,
    )
    return [
        {
            "provider": "azure-cosmos",
            "document_id": record.document_id,
            "partition_key": record.partition_key,
            "etag": record.etag,
            "updated_at": record.updated_at,
            "body": record.body,
        }
        for record in (build_document_record(item) for item in results)
    ]
