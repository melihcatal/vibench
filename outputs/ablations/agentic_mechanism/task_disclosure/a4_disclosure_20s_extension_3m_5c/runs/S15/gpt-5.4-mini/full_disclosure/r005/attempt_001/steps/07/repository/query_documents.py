import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import boto3
from boto3.dynamodb.conditions import Attr, Key


@dataclass
class QueryResult:
    field_name: str
    field_value: Any
    items: List[Dict[str, Any]]
    count: int
    scanned_count: int
    last_evaluated_key: Optional[Dict[str, Any]]


def _ddb_table_name() -> str:
    table_name = os.getenv("AWS_DYNAMODB_TABLE_NAME") or os.getenv("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise ValueError("Missing AWS_DYNAMODB_TABLE_NAME")
    return table_name


def _ddb_table():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    return boto3.resource("dynamodb", region_name=region).Table(_ddb_table_name())


def query_documents(field_name: str, field_value: Any, partition_key: bool = False) -> QueryResult:
    if not field_name:
        raise ValueError("field_name must be provided")
    table = _ddb_table()
    if partition_key:
        response = table.query(KeyConditionExpression=Key(field_name).eq(field_value))
    else:
        response = table.scan(FilterExpression=Attr(field_name).eq(field_value))
    items = response.get("Items", [])
    return QueryResult(
        field_name=field_name,
        field_value=field_value,
        items=items,
        count=response.get("Count", len(items)),
        scanned_count=response.get("ScannedCount", len(items)),
        last_evaluated_key=response.get("LastEvaluatedKey"),
    )


__all__ = ["QueryResult", "query_documents"]
