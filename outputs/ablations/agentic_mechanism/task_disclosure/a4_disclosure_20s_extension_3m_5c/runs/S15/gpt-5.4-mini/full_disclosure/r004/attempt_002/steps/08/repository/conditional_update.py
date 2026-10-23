import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError


def _table_name() -> str:
    value = os.getenv("AWS_DYNAMODB_TABLE") or os.getenv("DYNAMODB_TABLE")
    if not value:
        raise ValueError("AWS_DYNAMODB_TABLE is required")
    return value


def _client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    return boto3.resource("dynamodb", region_name=region).Table(_table_name())


def conditional_update(
    key: Dict[str, Any],
    update_expression: str,
    expression_attribute_values: Dict[str, Any],
    expression_attribute_names: Optional[Dict[str, str]] = None,
    condition_expression: Optional[str] = None,
    return_values: str = "ALL_NEW",
) -> Dict[str, Any]:
    params: Dict[str, Any] = {
        "Key": key,
        "UpdateExpression": update_expression,
        "ExpressionAttributeValues": expression_attribute_values,
        "ReturnValues": return_values,
    }
    if expression_attribute_names:
        params["ExpressionAttributeNames"] = expression_attribute_names
    if condition_expression:
        params["ConditionExpression"] = condition_expression
    try:
        response = _client().update_item(**params)
    except ClientError as exc:
        error = exc.response.get("Error", {})
        code = error.get("Code", "ClientError")
        message = error.get("Message", str(exc))
        raise RuntimeError(f"DynamoDB conditional update failed: {code}: {message}") from exc
    return response.get("Attributes", {})
