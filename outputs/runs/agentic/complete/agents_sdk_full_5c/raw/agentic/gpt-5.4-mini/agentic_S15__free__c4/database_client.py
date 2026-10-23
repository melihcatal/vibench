from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Optional

import boto3
from botocore.client import BaseClient
from botocore.config import Config


@dataclass(frozen=True)
class DynamoConfig:
    table_name: str
    region_name: str
    endpoint_url: Optional[str] = None


@lru_cache(maxsize=1)
def load_config() -> DynamoConfig:
    table_name = os.environ.get("DYNAMODB_TABLE_NAME", "managed-document-store")
    region_name = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
    endpoint_url = os.environ.get("DYNAMODB_ENDPOINT_URL")
    return DynamoConfig(table_name=table_name, region_name=region_name, endpoint_url=endpoint_url)


@lru_cache(maxsize=1)
def get_dynamodb_resource():
    config = load_config()
    return boto3.resource(
        "dynamodb",
        region_name=config.region_name,
        endpoint_url=config.endpoint_url,
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


@lru_cache(maxsize=1)
def get_table():
    return get_dynamodb_resource().Table(load_config().table_name)


@lru_cache(maxsize=1)
def get_dynamodb_client() -> BaseClient:
    config = load_config()
    return boto3.client(
        "dynamodb",
        region_name=config.region_name,
        endpoint_url=config.endpoint_url,
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


def provider_signal() -> str:
    return "aws_dynamodb"
