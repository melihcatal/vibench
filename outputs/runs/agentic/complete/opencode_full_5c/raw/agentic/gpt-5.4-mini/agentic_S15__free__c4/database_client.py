import os
from functools import lru_cache

import boto3


def get_table_name() -> str:
    return os.environ.get("DYNAMODB_TABLE_NAME", "managed_document_store")


def get_region_name() -> str:
    return os.environ.get(
        "AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    )


@lru_cache(maxsize=1)
def get_dynamodb_resource():
    return boto3.resource("dynamodb", region_name=get_region_name())


def get_dynamodb_table():
    return get_dynamodb_resource().Table(get_table_name())
