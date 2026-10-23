from __future__ import annotations

from typing import Any

from database_client import get_container_client
from database_models import DocumentQueryRequest
from database_models import normalize_document_payload


def query_documents(request: DocumentQueryRequest) -> list[dict[str, Any]]:
    container = get_container_client()
    parameters: list[dict[str, Any]] = []
    if request.partition_key is not None:
        query = "SELECT * FROM c WHERE c.partition_key = @partition_key"
        parameters.append({"name": "@partition_key", "value": request.partition_key})
    elif request.field_name is not None:
        query = f"SELECT * FROM c WHERE c[{request.field_name!r}] = @field_value"
        parameters.append({"name": "@field_value", "value": request.field_value})
    else:
        query = "SELECT * FROM c"
    items = container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True,
        max_item_count=request.limit,
    )
    results: list[dict[str, Any]] = []
    for item in items:
        record = normalize_document_payload(item)
        results.append(
            {
                "id": record.id,
                "partition_key": record.partition_key,
                "etag": record.version,
                "document": record.content,
            }
        )
        if len(results) >= request.limit:
            break
    return results
