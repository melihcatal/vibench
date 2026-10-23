from __future__ import annotations

from typing import Any, List

from database_client import get_container_client
from database_models import DocumentRecord, QueryRequest, normalize_documents


def query_documents(request: QueryRequest) -> List[DocumentRecord]:
    container = get_container_client()

    if request.partition_key:
        query = "SELECT * FROM c WHERE c.partitionKey = @partition_key"
        parameters = [{"name": "@partition_key", "value": request.partition_key}]
        cross_partition = False
    elif request.field_name:
        query = f"SELECT * FROM c WHERE c[{repr(request.field_name)}] = @field_value"
        parameters = [{"name": "@field_value", "value": request.field_value}]
        cross_partition = True
    else:
        query = "SELECT * FROM c"
        parameters = []
        cross_partition = True

    items = list(
        container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=cross_partition,
            max_item_count=request.limit,
        )
    )[: request.limit]
    return normalize_documents(items)
