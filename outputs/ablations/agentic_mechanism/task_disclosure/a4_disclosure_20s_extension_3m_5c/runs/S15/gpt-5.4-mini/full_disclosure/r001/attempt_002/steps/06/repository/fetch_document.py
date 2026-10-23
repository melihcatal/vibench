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


def fetch_document(identifier: Any, primary_key: Optional[str] = None) -> Dict[str, Any]:
    key_name = primary_key or _key_name()
    if identifier in (None, ""):
        raise ValueError("identifier must be provided")

    table = _client()
    response = table.get_item(Key={key_name: identifier})
    item = response.get("Item")
    if item is None:
        raise KeyError(f"document not found for {key_name}={identifier!r}")
    return item
