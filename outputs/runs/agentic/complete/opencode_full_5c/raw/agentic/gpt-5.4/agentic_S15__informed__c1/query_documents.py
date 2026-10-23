from __future__ import annotations

from typing import Any

from database_client import get_cosmos_container
from database_models import DocumentQueryRequest


def query_documents(
    field_name: str, field_value: Any, limit: int = 25
) -> list[dict[str, Any]]:
    container = get_cosmos_container()
    request = DocumentQueryRequest(
        field_name=field_name, field_value=field_value, limit=limit
    )
    query = f"SELECT * FROM c WHERE c[{repr(request.field_name)}] = @value OFFSET 0 LIMIT {int(request.limit)}"
    parameters = [{"name": "@value", "value": request.field_value}]
    return list(
        container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True,
        )
    )
