import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import boto3
from boto3.resources.base import ServiceResource
from botocore.client import BaseClient

DEFAULT_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
DEFAULT_TABLE_NAME = os.getenv("DDB_TABLE_NAME", "documents")
DEFAULT_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "document-archives")


@dataclass(frozen=True)
class DynamoConfig:
    region_name: str = DEFAULT_REGION
    table_name: str = DEFAULT_TABLE_NAME


@dataclass(frozen=True)
class S3Config:
    region_name: str = DEFAULT_REGION
    bucket_name: str = DEFAULT_BUCKET_NAME


@lru_cache(maxsize=1)
def get_session() -> boto3.Session:
    return boto3.Session(region_name=DEFAULT_REGION)


@lru_cache(maxsize=1)
def get_dynamodb_resource() -> ServiceResource:
    return get_session().resource("dynamodb", region_name=DEFAULT_REGION)


@lru_cache(maxsize=1)
def get_dynamodb_client() -> BaseClient:
    return get_session().client("dynamodb", region_name=DEFAULT_REGION)


@lru_cache(maxsize=1)
def get_s3_client() -> BaseClient:
    return get_session().client("s3", region_name=DEFAULT_REGION)


def get_table_name(table_name: Optional[str] = None) -> str:
    return table_name or DEFAULT_TABLE_NAME


def get_bucket_name(bucket_name: Optional[str] = None) -> str:
    return bucket_name or DEFAULT_BUCKET_NAME


def table_resource(table_name: Optional[str] = None):
    return get_dynamodb_resource().Table(get_table_name(table_name))


def document_key(identifier: str, sort_key: Optional[str] = None) -> Dict[str, Any]:
    key = {"document_id": identifier}
    if sort_key is not None:
        key["sort_key"] = sort_key
    return key
