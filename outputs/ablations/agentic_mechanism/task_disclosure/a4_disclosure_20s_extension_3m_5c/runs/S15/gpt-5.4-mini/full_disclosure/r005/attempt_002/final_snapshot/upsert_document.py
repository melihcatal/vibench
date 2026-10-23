import json
import os
from typing import Any, Dict, Optional

import requests


class UpsertDocumentError(Exception):
    pass


def _base_url() -> str:
    return os.environ.get("DYNAMODB_HTTP_BASE_URL", "https://dynamodb.us-east-1.amazonaws.com")


def _table_name() -> str:
    value = os.environ.get("DYNAMODB_TABLE_NAME")
    if not value:
        raise UpsertDocumentError("DYNAMODB_TABLE_NAME is required")
    return value


def _primary_key_name() -> str:
    return os.environ.get("DYNAMODB_PRIMARY_KEY", "id")


def _auth_headers() -> Dict[str, str]:
    headers = {"Content-Type": "application/x-amz-json-1.0", "X-Amz-Target": "DynamoDB_20120810.PutItem"}
    token = os.environ.get("AWS_SESSION_TOKEN")
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    if access_key and secret_key:
        headers["X-Provider"] = "aws-dynamodb"
    if token:
        headers["X-AWS-Session-Token"] = token
    return headers


def _to_ddb_value(value: Any) -> Dict[str, Any]:
    if value is None:
        return {"NULL": True}
    if isinstance(value, bool):
        return {"BOOL": value}
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return {"N": str(value)}
    if isinstance(value, str):
        return {"S": value}
    if isinstance(value, list):
        return {"L": [_to_ddb_value(item) for item in value]}
    if isinstance(value, dict):
        return {"M": {k: _to_ddb_value(v) for k, v in value.items()}}
    return {"S": json.dumps(value, ensure_ascii=False)}


def upsert_document(document: Dict[str, Any], identifier: Optional[Any] = None) -> Dict[str, Any]:
    key_name = _primary_key_name()
    doc = dict(document)
    if identifier is not None:
        doc[key_name] = identifier
    if key_name not in doc:
        raise UpsertDocumentError(f"Missing primary key field: {key_name}")
    item = {k: _to_ddb_value(v) for k, v in doc.items()}
    payload = {"TableName": _table_name(), "Item": item}
    response = requests.post(_base_url(), headers=_auth_headers(), data=json.dumps(payload), timeout=30)
    if response.status_code >= 400:
        raise UpsertDocumentError(response.text)
    return {"ok": True, "document": doc, "provider": "aws-dynamodb", "status_code": response.status_code}
