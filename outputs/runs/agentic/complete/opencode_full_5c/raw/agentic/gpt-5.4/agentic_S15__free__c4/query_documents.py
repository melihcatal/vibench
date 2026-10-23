from __future__ import annotations

from typing import Any

from database_client import get_container_client
from database_models import DocumentQueryRequest, parse_document_list


def query_documents(
    field_name: str, field_value: Any, partition_key: str | None = None, limit: int = 50
):
    request = DocumentQueryRequest(
        field_name=field_name,
        field_value=field_value,
        partition_key=partition_key,
        limit=limit,
    )
    container = get_container_client()
    query = f"SELECT * FROM c WHERE c[{repr(request.field_name)}] = @field_value"
    parameters = [{"name": "@field_value", "value": request.field_value}]
    items = list(
        container.query_items(
            query=query,
            parameters=parameters,
            partition_key=request.partition_key,
            enable_cross_partition_query=request.partition_key is None,
            max_item_count=request.limit,
        )
    )
    return parse_document_list(items)
