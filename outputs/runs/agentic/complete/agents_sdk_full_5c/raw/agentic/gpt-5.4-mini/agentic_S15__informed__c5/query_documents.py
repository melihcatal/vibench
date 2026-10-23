from __future__ import annotations

from typing import Any, Dict, List, Optional

from azure.cosmos.exceptions import CosmosHttpResponseError

from database_client import get_container_client
from database_models import NormalizedResponse


def query_documents(field_name: str, field_value: Any, database_name: str = "documents", container_name: str = "records", partition_key: Optional[str] = None) -> NormalizedResponse:
    container = get_container_client(database_name, container_name)
    query = f"SELECT * FROM c WHERE c.{field_name} = @value"
    params = [{"name": "@value", "value": field_value}]
    try:
        if partition_key is None:
            items = list(container.query_items(query=query, parameters=params, enable_cross_partition_query=True))
        else:
            items = list(container.query_items(query=query, parameters=params, partition_key=partition_key))
        return NormalizedResponse(ok=True, data={"items": items, "count": len(items)})
    except CosmosHttpResponseError as exc:
        return NormalizedResponse(ok=False, data={"error": str(exc), "status_code": getattr(exc, "status_code", None)})
