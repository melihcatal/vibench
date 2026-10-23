import os
from typing import Any, Dict, Optional

import boto3


def _client():
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    session = boto3.session.Session(region_name=region)
    return session.client("dynamodb")


def _to_dynamo(value: Any) -> Dict[str, Any]:
    if value is None:
        return {"NULL": True}
    if isinstance(value, bool):
        return {"BOOL": value}
    if isinstance(value, (int, float)):
        return {"N": str(value)}
    if isinstance(value, str):
        return {"S": value}
    if isinstance(value, dict):
        return {"M": {k: _to_dynamo(v) for k, v in value.items()}}
    if isinstance(value, list):
        return {"L": [_to_dynamo(v) for v in value]}
    raise TypeError(f"Unsupported value type: {type(value)!r}")


def conditional_update(
    table_name: str,
    key: Dict[str, Any],
    update_expression: str,
    expression_attribute_values: Dict[str, Any],
    expression_attribute_names: Optional[Dict[str, str]] = None,
    condition_expression: Optional[str] = None,
    return_values: str = "ALL_NEW",
) -> Dict[str, Any]:
    dynamo = _client()
    params: Dict[str, Any] = {
        "TableName": table_name,
        "Key": {k: _to_dynamo(v) for k, v in key.items()},
        "UpdateExpression": update_expression,
        "ExpressionAttributeValues": {k: _to_dynamo(v) for k, v in expression_attribute_values.items()},
        "ReturnValues": return_values,
    }
    if expression_attribute_names:
        params["ExpressionAttributeNames"] = expression_attribute_names
    if condition_expression:
        params["ConditionExpression"] = condition_expression
    return dynamo.update_item(**params)
