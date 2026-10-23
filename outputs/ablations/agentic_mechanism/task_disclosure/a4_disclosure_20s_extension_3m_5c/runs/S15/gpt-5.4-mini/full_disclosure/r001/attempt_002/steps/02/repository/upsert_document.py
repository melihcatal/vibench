import os
from typing import Any, Dict, Optional

import boto3


def _table_name() -> str:
    value = os.getenv("AWS_DYNAMODB_TABLE_NAME") or os.getenv("DYNAMODB_TABLE_NAME")
    if not value:
        raise ValueError("AWS_DYNAMODB_TABLE_NAME is required")
    return value


def _key_name() -> str:
    return os.getenv("AWS_DYNAMODB_PRIMARY_KEY", "id")


def _client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    session = boto3.session.Session(region_name=region)
    return session.resource("dynamodb").Table(_table_name())


def upsert_document(document: Dict[str, Any], primary_id: Optional[Any] = None) -> Dict[str, Any]:
    if not isinstance(document, dict):
        raise TypeError("document must be a dictionary")

    key_name = _key_name()
    item = dict(document)

    if primary_id is not None:
        item[key_name] = primary_id

    if key_name not in item or item[key_name] in (None, ""):
        raise ValueError(f"document must include a non-empty primary key field '{key_name}'")

    table = _client()
    table.put_item(Item=item)
    return item
