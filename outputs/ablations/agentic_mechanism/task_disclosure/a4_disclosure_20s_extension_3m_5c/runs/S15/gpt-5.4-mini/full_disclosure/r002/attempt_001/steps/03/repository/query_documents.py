import os
from decimal import Decimal
from typing import Any, Dict, List, Optional

import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import BotoCoreError, ClientError


class QueryDocumentsError(Exception):
    pass


def _table_name() -> str:
    table_name = os.getenv("DYNAMODB_TABLE_NAME") or os.getenv("AWS_DYNAMODB_TABLE_NAME")
    if not table_name:
        raise QueryDocumentsError("Missing DYNAMODB_TABLE_NAME")
    return table_name


def _primary_key_name() -> str:
    return os.getenv("DYNAMODB_PRIMARY_KEY", "id")


def _dynamodb_resource():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    return boto3.resource("dynamodb", region_name=region)


def _normalize(value: Any) -> Any:
    if isinstance(value, Decimal):
        if value % 1 == 0:
            return int(value)
        return float(value)
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    if isinstance(value, dict):
        return {key: _normalize(item) for key, item in value.items()}
    return value


def query_documents(
    field_name: str,
    field_value: Any,
    *,
    use_partition_key: bool = False,
    limit: Optional[int] = None,
    index_name: Optional[str] = None,
) -> Dict[str, Any]:
    if not field_name:
        raise QueryDocumentsError("Missing field_name")

    table = _dynamodb_resource().Table(_table_name())
    try:
        if use_partition_key:
            expression = Key(field_name).eq(field_value)
            kwargs: Dict[str, Any] = {"KeyConditionExpression": expression}
            if index_name:
                kwargs["IndexName"] = index_name
            if limit is not None:
                kwargs["Limit"] = limit
            response = table.query(**kwargs)
        else:
            expression = Attr(field_name).eq(field_value)
            kwargs = {"FilterExpression": expression}
            if limit is not None:
                kwargs["Limit"] = limit
            response = table.scan(**kwargs)
    except (BotoCoreError, ClientError) as exc:
        raise QueryDocumentsError(str(exc)) from exc

    items: List[Dict[str, Any]] = [_normalize(item) for item in response.get("Items", [])]
    return {
        "ok": True,
        "table": _table_name(),
        "field_name": field_name,
        "field_value": _normalize(field_value),
        "use_partition_key": use_partition_key,
        "count": response.get("Count", len(items)),
        "scanned_count": response.get("ScannedCount"),
        "documents": items,
        "response": _normalize(response),
    }
