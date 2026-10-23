import os
from functools import lru_cache
from typing import Any
import boto3


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


@lru_cache(maxsize=1)
def get_dynamodb_resource():
    region = _env("AWS_REGION", _env("AWS_DEFAULT_REGION", "us-east-1"))
    return boto3.resource("dynamodb", region_name=region)


@lru_cache(maxsize=1)
def get_dynamodb_table():
    table_name = _env("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise RuntimeError("DYNAMODB_TABLE_NAME is required")
    return get_dynamodb_resource().Table(table_name)


def get_config() -> dict[str, Any]:
    return {"table_name": _env("DYNAMODB_TABLE_NAME"), "region": _env("AWS_REGION", _env("AWS_DEFAULT_REGION", "us-east-1"))}
