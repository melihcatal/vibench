from __future__ import annotations

from typing import List
from database_client import get_container, get_partition_key_field
from database_models import DocumentRecord, QueryRequest


PROVIDER = "Azure Cosmos DB"


def query_documents(request: QueryRequest) -> List[DocumentRecord]:
    container = get_container()
    partition_key_field = get_partition_key_field()

    if request.partition_key is not None:
        query = f"SELECT * FROM c WHERE c.{partition_key_field} = @partition_key"
        parameters = [{"name": "@partition_key", "value": request.partition_key}]
    elif request.field_name is not None:
        query = f"SELECT * FROM c WHERE c[{repr(request.field_name)}] = @field_value"
        parameters = [{"name": "@field_value", "value": request.field_value}]
    else:
        query = "SELECT * FROM c"
        parameters = []

    items = list(
        container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True,
            max_item_count=request.limit,
        )
    )
    return [DocumentRecord.from_cosmos_item(item, partition_key_field=partition_key_field) for item in items[: request.limit]]
