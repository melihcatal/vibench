from __future__ import annotations

from boto3.dynamodb.conditions import Attr

from database_client import get_table, service_error_payload
from database_models import OperationResponse, QueryRequest


def query_documents(request: QueryRequest) -> OperationResponse:
    try:
        table = get_table(request.table_name)
        response = table.scan(
            FilterExpression=Attr(request.field_name).eq(request.field_value),
            Limit=request.limit,
        )
        items = response.get("Items", [])
        return OperationResponse(ok=True, data={"documents": items, "count": len(items)})
    except Exception as exc:
        return OperationResponse(ok=False, error=service_error_payload(exc))
