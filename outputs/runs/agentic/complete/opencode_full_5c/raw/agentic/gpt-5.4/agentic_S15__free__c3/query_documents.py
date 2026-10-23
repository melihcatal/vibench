from typing import Any, Dict, List

from database_client import get_cosmos_container
from database_models import QueryRequest


def query_documents(
    field_name: str, field_value: Any, limit: int = 25, partition_key: Any = None
) -> Dict[str, Any]:
    request = QueryRequest.create(
        field_name=field_name,
        field_value=field_value,
        limit=limit,
        partition_key=partition_key,
    )
    container = get_cosmos_container()
    query = f"SELECT TOP @limit * FROM c WHERE c[{repr(request.field_name)}] = @value"
    parameters = [
        {"name": "@limit", "value": request.limit},
        {"name": "@value", "value": request.field_value},
    ]
    options = {
        "query": query,
        "parameters": parameters,
        "enable_cross_partition_query": request.partition_key is None,
    }
    if request.partition_key is not None:
        options["partition_key"] = request.partition_key
    items: List[Dict[str, Any]] = list(container.query_items(**options))
    return {
        "provider": "azure-cosmos-db",
        "count": len(items),
        "items": items,
        "field": request.field_name,
        "partitionKey": request.partition_key,
    }
