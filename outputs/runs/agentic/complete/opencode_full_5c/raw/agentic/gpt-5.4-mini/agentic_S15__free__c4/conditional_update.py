from typing import Any, Dict

from botocore.exceptions import ClientError

from database_client import get_dynamodb_table
from database_models import primary_key, response_payload


def conditional_update(
    document_id: str, updates: Dict[str, Any], expected_version: int = None
) -> Dict[str, Any]:
    table = get_dynamodb_table()
    expr_names = {}
    expr_values = {}
    parts = []
    for key, value in updates.items():
        name_key = f"#{key}"
        value_key = f":{key}"
        expr_names[name_key] = key
        expr_values[value_key] = value
        parts.append(f"{name_key} = {value_key}")
    update_expression = "SET " + ", ".join(parts)
    condition_expression = None
    if expected_version is not None:
        expr_values[":expected_version"] = expected_version
        condition_expression = "version = :expected_version"
    try:
        kwargs = dict(
            Key=primary_key(document_id),
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expr_values,
            ReturnValues="ALL_NEW",
        )
        if expr_names:
            kwargs["ExpressionAttributeNames"] = expr_names
        if condition_expression:
            kwargs["ConditionExpression"] = condition_expression
        result = table.update_item(**kwargs)
        return response_payload(True, data={"document": result.get("Attributes", {})})
    except ClientError as exc:
        return response_payload(False, error=str(exc))


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return conditional_update(
        event["document_id"], event.get("updates", {}), event.get("expected_version")
    )
