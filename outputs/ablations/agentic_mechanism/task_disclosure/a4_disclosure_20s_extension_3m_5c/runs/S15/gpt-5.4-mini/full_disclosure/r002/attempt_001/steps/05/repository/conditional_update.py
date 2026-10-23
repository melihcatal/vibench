import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError


def _dynamodb_resource():
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    return boto3.resource("dynamodb", region_name=region)


def conditional_update(table_name: str, key: Dict[str, Any], update_expression: str, expression_attribute_values: Dict[str, Any], condition_expression: Optional[str] = None, expression_attribute_names: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    table = _dynamodb_resource().Table(table_name)
    params: Dict[str, Any] = {
        "Key": key,
        "UpdateExpression": update_expression,
        "ExpressionAttributeValues": expression_attribute_values,
        "ReturnValues": "ALL_NEW",
    }
    if condition_expression is not None:
        params["ConditionExpression"] = condition_expression
    if expression_attribute_names is not None:
        params["ExpressionAttributeNames"] = expression_attribute_names
    try:
        response = table.update_item(**params)
        return response.get("Attributes", {})
    except ClientError:
        raise
