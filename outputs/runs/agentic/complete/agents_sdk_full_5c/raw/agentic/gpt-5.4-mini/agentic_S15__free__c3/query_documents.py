from __future__ import annotations

from typing import Any, Dict, List

from boto3.dynamodb.conditions import Attr

from database_client import get_table, get_table_name
from database_models import DocumentQueryRequest, OperationResponse


def query_documents(field_name: str, field_value: Any, table_name: str | None = None, limit: int | None = None) -> OperationResponse:
    request = DocumentQueryRequest(field_name=field_name, field_value=field_value, table_name=table_name, limit=limit)
    table = get_table(request.table_name)
    expression = Attr(request.field_name).eq(request.field_value)
    scan_kwargs: Dict[str, Any] = {"FilterExpression": expression}
    if request.limit:
        scan_kwargs["Limit"] = request.limit
    result = table.scan(**scan_kwargs)
    items: List[Dict[str, Any]] = result.get("Items", [])
    return OperationResponse(ok=True, data={"table_name": get_table_name(request.table_name), "items": items, "count": len(items)})
