import json
import os
from typing import Any, Dict, List, Optional

import boto3


def _table_name() -> str:
    table = os.environ.get("DYNAMODB_TABLE_NAME") or os.environ.get("AWS_DYNAMODB_TABLE_NAME")
    if not table:
        raise ValueError("DYNAMODB_TABLE_NAME is required")
    return table


def _client():
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    if region:
        return boto3.resource("dynamodb", region_name=region).Table(_table_name())
    return boto3.resource("dynamodb").Table(_table_name())


def _normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    return json.loads(json.dumps(item, default=str))


def query_documents(
    field_name: str,
    field_value: Any,
    partition_key_name: Optional[str] = None,
    limit: Optional[int] = None,
    index_name: Optional[str] = None,
) -> List[Dict[str, Any]]:
    table = _client()
    expression_attribute_values = {":v": field_value}
    expression_attribute_names = {"#f": field_name}

    if partition_key_name and partition_key_name == field_name and not index_name:
        response = table.query(
            KeyConditionExpression="#f = :v",
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            Limit=limit if limit and limit > 0 else None,
        )
        return [_normalize_item(item) for item in response.get("Items", [])]

    kwargs: Dict[str, Any] = {
        "FilterExpression": "#f = :v",
        "ExpressionAttributeNames": expression_attribute_names,
        "ExpressionAttributeValues": expression_attribute_values,
    }
    if index_name:
        kwargs["IndexName"] = index_name
    if limit and limit > 0:
        kwargs["Limit"] = limit

    response = table.scan(**kwargs)
    return [_normalize_item(item) for item in response.get("Items", [])]


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    field_name = event["field_name"]
    field_value = event["field_value"]
    partition_key_name = event.get("partition_key_name")
    limit = event.get("limit")
    index_name = event.get("index_name")
    items = query_documents(field_name, field_value, partition_key_name, limit, index_name)
    return {"items": items, "count": len(items)}
