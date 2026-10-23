from __future__ import annotations

from typing import Any, List

from database_client import get_container, get_partition_field
from database_models import QueryRequest, responses_from_items



def query_documents(request: QueryRequest) -> List[dict[str, Any]]:
    container = get_container()
    partition_field = get_partition_field()
    parameters = [{"name": "@field_value", "value": request.field_value}]
    query = f"SELECT * FROM c WHERE c[{repr(request.field_name)}] = @field_value"
    if request.partition_key is not None and partition_field:
        query += " AND c[@partition_field] = @partition_value"
        parameters.extend(
            [
                {"name": "@partition_field", "value": partition_field},
                {"name": "@partition_value", "value": request.partition_key},
            ]
        )
    items = list(
        container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=request.partition_key is None,
            max_item_count=request.max_items,
        )
    )
    return [response.__dict__ for response in responses_from_items(items, partition_field=partition_field)]



def query_documents_by_field(field_name: str, field_value: Any, partition_key: str | None = None, max_items: int = 100) -> List[dict[str, Any]]:
    return query_documents(QueryRequest(field_name=field_name, field_value=field_value, partition_key=partition_key, max_items=max_items))
