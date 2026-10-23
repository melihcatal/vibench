from typing import Any, Dict, List

from database_client import get_container
from database_models import DocumentOperationResponse, DocumentQueryRequest, coerce_list


def query_documents(field_name: str, field_value: Any, partition_key: str = None, limit: int = 20) -> DocumentOperationResponse:
    request = DocumentQueryRequest(field_name=field_name, field_value=field_value, partition_key=partition_key, limit=limit)
    container = get_container()
    query = f"SELECT * FROM c WHERE c.{request.field_name} = @value"
    parameters = [{"name": "@value", "value": request.field_value}]
    if request.partition_key is not None:
        query += " AND c.partition_key = @partition_key"
        parameters.append({"name": "@partition_key", "value": request.partition_key})
    items = list(container.query_items(query=query, parameters=parameters, enable_cross_partition_query=request.partition_key is None))
    return DocumentOperationResponse(ok=True, document={"items": coerce_list(items)[: request.limit]}, matched_count=len(items), message="queried")


if __name__ == "__main__":
    raise SystemExit("This module exposes query_documents() for Cosmos DB queries.")
