from __future__ import annotations

from typing import Any, Dict

from database_client import get_table, service_error_payload
from database_models import ConditionalUpdateRequest, OperationResponse, merge_updates


def conditional_update(request: ConditionalUpdateRequest) -> OperationResponse:
    try:
        table = get_table(request.table_name)
        key = {"document_id": request.key.document_id}
        if request.key.partition_key is not None:
            key["partition_key"] = request.key.partition_key

        update_expression_parts = []
        expression_values: Dict[str, Any] = {}
        expression_names: Dict[str, str] = {}
        for idx, (field, value) in enumerate(request.updates.items()):
            name_key = f"#f{idx}"
            value_key = f":v{idx}"
            expression_names[name_key] = field
            expression_values[value_key] = value
            update_expression_parts.append(f"{name_key} = {value_key}")

        update_expression_parts.append("updated_at = :updated_at")
        expression_values[":updated_at"] = __import__("database_models").utc_now_iso()

        if request.expected_version is not None:
            expression_names["#version"] = "version"
            expression_values[":expected_version"] = request.expected_version
            condition = "#version = :expected_version"
        else:
            condition = None

        update_expr = "SET " + ", ".join(update_expression_parts)
        params = {
            "Key": key,
            "UpdateExpression": update_expr,
            "ExpressionAttributeValues": expression_values,
            "ReturnValues": "ALL_NEW",
        }
        if expression_names:
            params["ExpressionAttributeNames"] = expression_names
        if condition:
            params["ConditionExpression"] = condition
        response = table.update_item(**params)
        return OperationResponse(ok=True, data={"document": response.get("Attributes", {})})
    except Exception as exc:
        return OperationResponse(ok=False, error=service_error_payload(exc))
