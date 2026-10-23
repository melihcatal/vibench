from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Dict, Iterable, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from database_models import normalize_document

DYNAMODB_TABLE_ENV = "DYNAMODB_TABLE_NAME"
DYNAMODB_REGION_ENV = "AWS_REGION"
DYNAMODB_ENDPOINT_ENV = "DYNAMODB_ENDPOINT_URL"


@lru_cache(maxsize=1)
def get_dynamodb_resource():
    region_name = os.getenv(DYNAMODB_REGION_ENV) or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    endpoint_url = os.getenv(DYNAMODB_ENDPOINT_ENV)
    return boto3.resource("dynamodb", region_name=region_name, endpoint_url=endpoint_url)


def get_table_name(default: str = "documents") -> str:
    return os.getenv(DYNAMODB_TABLE_ENV, default)


def get_table(table_name: Optional[str] = None):
    resource = get_dynamodb_resource()
    return resource.Table(table_name or get_table_name())


def serialize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    return normalize_document(item)


def db_error_message(error: Exception) -> str:
    if isinstance(error, ClientError):
        return error.response.get("Error", {}).get("Message", str(error))
    if isinstance(error, BotoCoreError):
        return str(error)
    return str(error)
