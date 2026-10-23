import os
from typing import Any, Dict, List, Optional

import boto3
from boto3.dynamodb.conditions import Attr, Key


class QueryDocumentsError(Exception):
    pass


def _table_name() -> str:
    table = os.getenv("AWS_DYNAMODB_TABLE_NAME") or os.getenv("DYNAMODB_TABLE_NAME")
    if not table:
        raise QueryDocumentsError("Missing AWS_DYNAMODB_TABLE_NAME")
    return table


def _dynamodb_resource():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    session_kwargs: Dict[str, Any] = {}
    if region:
        session_kwargs["region_name"] = region
    session = boto3.session.Session(**session_kwargs)
    return session.resource("dynamodb")


def _normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    return item


def query_documents(
    field_name: str,
    field_value: Any,
    *,
    partition_key_name: Optional[str] = None,
    limit: Optional[int] = None,
    descending: bool = False,
) -> List[Dict[str, Any]]:
    if not field_name:
        raise QueryDocumentsError("field_name is required")

    table = _dynamodb_resource().Table(_table_name())

    if partition_key_name and partition_key_name == field_name:
        kwargs: Dict[str, Any] = {
            "KeyConditionExpression": Key(field_name).eq(field_value),
            "ScanIndexForward": not descending,
        }
        if limit is not None:
            kwargs["Limit"] = limit
        response = table.query(**kwargs)
        items = response.get("Items", [])
        return [_normalize_item(item) for item in items]

    scan_kwargs: Dict[str, Any] = {
        "FilterExpression": Attr(field_name).eq(field_value),
    }
    if limit is not None:
        scan_kwargs["Limit"] = limit
    response = table.scan(**scan_kwargs)
    items = response.get("Items", [])
    return [_normalize_item(item) for item in items]
