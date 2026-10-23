from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Dict, Optional

import boto3
from botocore.client import BaseClient

DEFAULT_TABLE_NAME = os.getenv("NOSQL_TABLE_NAME", "managed_document_store")
DEFAULT_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


@lru_cache(maxsize=1)
def get_dynamodb_client() -> BaseClient:
    return boto3.client("dynamodb", region_name=DEFAULT_REGION)


@lru_cache(maxsize=1)
def get_dynamodb_resource():
    return boto3.resource("dynamodb", region_name=DEFAULT_REGION)


def get_table_name(table_name: Optional[str] = None) -> str:
    return table_name or DEFAULT_TABLE_NAME


def get_table(table_name: Optional[str] = None):
    return get_dynamodb_resource().Table(get_table_name(table_name))


def env_config() -> Dict[str, Any]:
    return {
        "table_name": DEFAULT_TABLE_NAME,
        "region": DEFAULT_REGION,
        "service": "amazon-dynamodb",
        "provider": "aws",
    }
