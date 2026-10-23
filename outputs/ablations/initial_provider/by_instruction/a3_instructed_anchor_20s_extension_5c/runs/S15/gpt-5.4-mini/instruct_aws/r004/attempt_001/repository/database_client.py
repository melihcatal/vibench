import os
from functools import lru_cache

import boto3


def table_name() -> str:
    return os.environ.get("DYNAMODB_TABLE_NAME", "documents")


@lru_cache(maxsize=1)
def dynamodb_resource():
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
    return boto3.resource("dynamodb", region_name=region)


def table():
    return dynamodb_resource().Table(table_name())


def json_content_type() -> str:
    return "application/json"
