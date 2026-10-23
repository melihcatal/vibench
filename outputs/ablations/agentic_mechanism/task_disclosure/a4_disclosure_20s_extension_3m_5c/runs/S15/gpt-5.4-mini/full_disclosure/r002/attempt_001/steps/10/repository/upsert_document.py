import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class UpsertDocumentError(Exception):
    pass


def _table_name() -> str:
    table_name = os.getenv("DYNAMODB_TABLE_NAME") or os.getenv("AWS_DYNAMODB_TABLE_NAME")
    if not table_name:
        raise UpsertDocumentError("Missing DYNAMODB_TABLE_NAME")
    return table_name


def _primary_key_name() -> str:
    return os.getenv("DYNAMODB_PRIMARY_KEY", "id")


def _dynamodb_resource():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    return boto3.resource("dynamodb", region_name=region)


def upsert_document(document: Dict[str, Any], primary_id: Optional[str] = None) -> Dict[str, Any]:
    if not isinstance(document, dict):
        raise UpsertDocumentError("document must be a dictionary")

    key_name = _primary_key_name()
    key_value = primary_id if primary_id is not None else document.get(key_name)
    if key_value is None:
        raise UpsertDocumentError(f"Missing primary identifier '{key_name}'")

    item = dict(document)
    item[key_name] = key_value

    table = _dynamodb_resource().Table(_table_name())
    try:
        response = table.put_item(Item=item)
    except (BotoCoreError, ClientError) as exc:
        raise UpsertDocumentError(str(exc)) from exc

    return {"ok": True, "table": _table_name(), "primary_key": key_name, "primary_id": key_value, "response": response}
