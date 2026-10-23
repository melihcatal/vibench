import os
from functools import lru_cache

import boto3


def table_name() -> str:
    return os.environ.get("DYNAMODB_TABLE_NAME", "documents")


def region_name() -> str:
    return os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"


@lru_cache(maxsize=1)
def dynamodb_resource():
    return boto3.resource("dynamodb", region_name=region_name())


@lru_cache(maxsize=1)
def dynamodb_client():
    return boto3.client("dynamodb", region_name=region_name())


def table():
    return dynamodb_resource().Table(table_name())
