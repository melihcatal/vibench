import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class FetchDocumentError(Exception):
    pass


def _table_name() -> str:
    table_name = os.getenv("DYNAMODB_TABLE_NAME") or os.getenv("AWS_DYNAMODB_TABLE_NAME")
    if not table_name:
        raise FetchDocumentError("Missing DYNAMODB_TABLE_NAME")
    return table_name


def _primary_key_name() -> str:
    return os.getenv("DYNAMODB_PRIMARY_KEY", "id")


def _dynamodb_resource():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    return boto3.resource("dynamodb", region_name=region)


def fetch_document(identifier: Any, primary_key: Optional[str] = None) -> Dict[str, Any]:
    key_name = primary_key or _primary_key_name()
    if identifier is None:
        raise FetchDocumentError(f"Missing primary identifier '{key_name}'")

    table = _dynamodb_resource().Table(_table_name())
    try:
        response = table.get_item(Key={key_name: identifier})
    except (BotoCoreError, ClientError) as exc:
        raise FetchDocumentError(str(exc)) from exc

    item = response.get("Item")
    if item is None:
        return {"ok": False, "found": False, "table": _table_name(), "primary_key": key_name, "primary_id": identifier, "document": None}

    return {"ok": True, "found": True, "table": _table_name(), "primary_key": key_name, "primary_id": identifier, "document": item, "response": response}
