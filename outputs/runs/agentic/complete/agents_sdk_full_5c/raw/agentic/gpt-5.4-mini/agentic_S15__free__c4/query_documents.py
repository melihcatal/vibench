from __future__ import annotations

from typing import Any, Dict, List

from boto3.dynamodb.conditions import Attr, Key

from database_client import get_table
from database_models import deserialize_item


def query_documents(field_name: str, field_value: Any, *, index_name: str | None = None) -> List[Dict[str, Any]]:
    table = get_table()
    expression = Key(field_name).eq(field_value)
    params: Dict[str, Any] = {"KeyConditionExpression": expression}
    if index_name:
        params["IndexName"] = index_name
    response = table.query(**params)
    items = response.get("Items", [])
    if items:
        return [deserialize_item(item) for item in items]
    scan_response = table.scan(FilterExpression=Attr(field_name).eq(field_value))
    return [deserialize_item(item) for item in scan_response.get("Items", [])]
