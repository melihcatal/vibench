import os
from functools import lru_cache

import boto3


@lru_cache(maxsize=1)
def get_table_name() -> str:
    return os.getenv("DYNAMODB_TABLE_NAME", "documents")


@lru_cache(maxsize=1)
def get_dynamodb_resource():
    return boto3.resource("dynamodb")


def get_table():
    return get_dynamodb_resource().Table(get_table_name())
