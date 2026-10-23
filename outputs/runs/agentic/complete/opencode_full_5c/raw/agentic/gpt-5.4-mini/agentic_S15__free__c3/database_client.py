import os
from functools import lru_cache

import boto3


def get_region():
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


@lru_cache(maxsize=1)
def get_dynamodb_resource():
    return boto3.resource("dynamodb", region_name=get_region())


def get_table_name():
    name = os.getenv("DYNAMODB_TABLE_NAME")
    if not name:
        raise ValueError("DYNAMODB_TABLE_NAME is required")
    return name


def get_table():
    return get_dynamodb_resource().Table(get_table_name())
