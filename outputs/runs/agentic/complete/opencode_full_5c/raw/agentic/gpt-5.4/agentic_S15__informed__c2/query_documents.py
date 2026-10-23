from __future__ import annotations

from typing import Any

from database_client import get_container, sanitize_query_value
from database_models import DocumentQueryRequest, DocumentRecord


def query_documents(
    field_name: str, field_value: Any, partition_key: str | None = None, limit: int = 25
) -> list[dict[str, Any]]:
    if not field_name or not field_name.replace("_", "").isalnum():
        raise ValueError("field_name must be a simple identifier")
    request = DocumentQueryRequest(
        field_name=field_name,
        field_value=sanitize_query_value(field_value),
        partition_key=partition_key,
        limit=limit,
    )
    container = get_container()
    if request.partition_key is not None:
        query = f"SELECT TOP @limit * FROM c WHERE c.pk = @pk AND c.{request.field_name} = @value"
        parameters = [
            {"name": "@limit", "value": request.limit},
            {"name": "@pk", "value": request.partition_key},
            {"name": "@value", "value": request.field_value},
        ]
    else:
        query = f"SELECT TOP @limit * FROM c WHERE c.{request.field_name} = @value"
        parameters = [
            {"name": "@limit", "value": request.limit},
            {"name": "@value", "value": request.field_value},
        ]
    items = container.query_items(
        query=query, parameters=parameters, enable_cross_partition_query=True
    )
    return [DocumentRecord.from_item(item).content for item in items]
