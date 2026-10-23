import os
from functools import lru_cache

import boto3


def get_table_name() -> str:
    value = os.environ.get("AWS_DYNAMODB_TABLE_NAME") or os.environ.get(
        "DYNAMODB_TABLE_NAME"
    )
    if not value:
        raise ValueError("AWS_DYNAMODB_TABLE_NAME is required")
    return value


@lru_cache(maxsize=1)
def get_dynamodb_resource():
    region = (
        os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or "us-east-1"
    )
    return boto3.resource("dynamodb", region_name=region)


def get_table():
    return get_dynamodb_resource().Table(get_table_name())
