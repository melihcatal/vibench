from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from database_client import get_container_client
from database_models import QueryResult
from database_models import normalize_documents


def query_documents(
    field_name: str,
    field_value: Any,
    partition_key: Optional[str] = None,
    limit: int = 50,
) -> QueryResult:
    container = get_container_client()
    query = f"SELECT * FROM c WHERE c[{repr(field_name)}] = @field_value"
    parameters: List[Dict[str, Any]] = [{"name": "@field_value", "value": field_value}]
    options: Dict[str, Any] = {"max_item_count": int(limit)}
    if partition_key is not None:
        options["partition_key"] = str(partition_key)
    items = list(container.query_items(query=query, parameters=parameters, **options))
    normalized = normalize_documents(items)
    return QueryResult(items=normalized, count=len(normalized))
