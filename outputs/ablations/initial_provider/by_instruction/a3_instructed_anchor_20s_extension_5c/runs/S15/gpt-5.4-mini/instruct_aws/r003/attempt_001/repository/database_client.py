import os
from functools import lru_cache

import boto3


def table_name() -> str:
    return os.environ.get("AWS_DYNAMODB_TABLE", "documents")


def region_name() -> str:
    return os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))


@lru_cache(maxsize=1)
def dynamodb_resource():
    return boto3.resource("dynamodb", region_name=region_name())


@lru_cache(maxsize=1)
def dynamodb_client():
    return boto3.client("dynamodb", region_name=region_name())


def documents_table():
    return dynamodb_resource().Table(table_name())
