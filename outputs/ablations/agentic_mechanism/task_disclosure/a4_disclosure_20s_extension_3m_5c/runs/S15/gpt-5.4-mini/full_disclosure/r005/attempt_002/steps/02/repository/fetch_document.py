import json
import os
from typing import Any, Dict, Optional

import requests


class FetchDocumentError(Exception):
    pass


def _base_url() -> str:
    return os.environ.get("DYNAMODB_HTTP_BASE_URL", "https://dynamodb.us-east-1.amazonaws.com")


def _table_name() -> str:
    value = os.environ.get("DYNAMODB_TABLE_NAME")
    if not value:
        raise FetchDocumentError("DYNAMODB_TABLE_NAME is required")
    return value


def _primary_key_name() -> str:
    return os.environ.get("DYNAMODB_PRIMARY_KEY", "id")


def _auth_headers() -> Dict[str, str]:
    headers = {"Content-Type": "application/x-amz-json-1.0", "X-Amz-Target": "DynamoDB_20120810.GetItem"}
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


def _from_ddb_value(value: Dict[str, Any]) -> Any:
    if "S" in value:
        return value["S"]
    if "N" in value:
        number = value["N"]
        return int(number) if number.isdigit() or (number.startswith("-") and number[1:].isdigit()) else float(number)
    if "BOOL" in value:
        return value["BOOL"]
    if "NULL" in value:
        return None
    if "L" in value:
        return [_from_ddb_value(item) for item in value["L"]]
    if "M" in value:
        return {k: _from_ddb_value(v) for k, v in value["M"].items()}
    if "SS" in value:
        return list(value["SS"])
    if "NS" in value:
        return [_from_ddb_value({"N": item}) for item in value["NS"]]
    return value


def fetch_document(identifier: Any) -> Dict[str, Any]:
    key_name = _primary_key_name()
    payload = {"TableName": _table_name(), "Key": {key_name: _to_ddb_value(identifier)}, "ConsistentRead": True}
    response = requests.post(_base_url(), headers=_auth_headers(), data=json.dumps(payload), timeout=30)
    if response.status_code >= 400:
        raise FetchDocumentError(response.text)
    data = response.json() if response.content else {}
    item = data.get("Item")
    if not item:
        return {"ok": False, "found": False, "provider": "aws-dynamodb", "document": None}
    document = {k: _from_ddb_value(v) for k, v in item.items()}
    return {"ok": True, "found": True, "provider": "aws-dynamodb", "document": document}
