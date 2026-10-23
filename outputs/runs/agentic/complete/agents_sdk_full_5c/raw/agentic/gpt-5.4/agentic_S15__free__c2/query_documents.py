from __future__ import annotations

from typing import Any, Optional

from azure.cosmos.exceptions import CosmosHttpResponseError

from database_client import get_container
from database_models import OperationResult, QueryRequest, normalize_records


def query_documents(field_name: Optional[str] = None, field_value: Any = None, partition_key: Optional[str] = None, limit: int = 50) -> OperationResult:
    request = QueryRequest(field_name=field_name, field_value=field_value, partition_key=partition_key, limit=limit)
    container = get_container(create_if_missing=False)

    query = "SELECT TOP @limit * FROM c"
    parameters = [{"name": "@limit", "value": request.limit}]
    predicates = []

    if request.partition_key is not None:
        predicates.append("c.partitionKey = @partitionKey")
        parameters.append({"name": "@partitionKey", "value": request.partition_key})
    if request.field_name is not None and request.field_value is not None:
        predicates.append(f"c[{repr(request.field_name)}] = @fieldValue")
        parameters.append({"name": "@fieldValue", "value": request.field_value})

    if predicates:
        query += " WHERE " + " AND ".join(predicates)

    try:
        items = list(
            container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=request.partition_key is None,
            )
        )
        headers = container.client_connection.last_response_headers
        return OperationResult(
            ok=True,
            items=normalize_records(items),
            request_charge=float(headers.get("x-ms-request-charge", 0.0)),
            message="queried from Azure Cosmos DB",
        )
    except CosmosHttpResponseError as exc:
        return OperationResult(ok=False, message=str(exc))
