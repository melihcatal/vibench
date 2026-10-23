from __future__ import annotations

from typing import Any, Dict

from botocore.exceptions import ClientError

from database_client import get_table, get_table_name
from database_models import DocumentConditionalUpdateRequest, OperationResponse


def conditional_update(document_id: str, updates: Dict[str, Any], expected_version: int | None = None, table_name: str | None = None) -> OperationResponse:
    request = DocumentConditionalUpdateRequest(document_id=document_id, updates=updates, expected_version=expected_version, table_name=table_name)
    table = get_table(request.table_name)
    expr_values: Dict[str, Any] = {f":v{i}": v for i, v in enumerate(request.updates.values())}
    update_expr = "SET " + ", ".join(f"{k} = :v{i}" for i, k in enumerate(request.updates.keys()))
    condition_expr = None
    if request.expected_version is not None:
        condition_expr = "version = :expected_version"
        expr_values[":expected_version"] = request.expected_version
        update_expr += ", version = version + :one"
        expr_values[":one"] = 1
    try:
        result = table.update_item(
            Key={"document_id": request.document_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_values,
            ConditionExpression=condition_expr,
            ReturnValues="ALL_NEW",
        )
        return OperationResponse(ok=True, data={"table_name": get_table_name(request.table_name), "item": result.get("Attributes", {})})
    except ClientError as exc:
        return OperationResponse(ok=False, error=str(exc))
