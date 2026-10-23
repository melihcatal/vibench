"""Query documents by field value or partition-style key in Azure Cosmos DB."""
from __future__ import annotations

from typing import Any, Dict, Optional

from database_client import get_container, load_cosmos_config
from database_models import QueryResponse, normalize_query_value


def query_documents(field_name: str, field_value: Any, partition_key: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
    config = load_cosmos_config()
    container = get_container(config)
    value = normalize_query_value(field_value)
    if partition_key is not None:
        query = f"SELECT * FROM c WHERE c.{field_name} = @value AND c.{config.partition_key_path.lstrip('/')} = @pk"
        params = [{"name": "@value", "value": value}, {"name": "@pk", "value": partition_key}]
    else:
        query = f"SELECT * FROM c WHERE c.{field_name} = @value"
        params = [{"name": "@value", "value": value}]
    items = list(container.query_items(query=query, parameters=params, enable_cross_partition_query=True))[:limit]
    return QueryResponse(documents=items, count=len(items)).as_dict()
