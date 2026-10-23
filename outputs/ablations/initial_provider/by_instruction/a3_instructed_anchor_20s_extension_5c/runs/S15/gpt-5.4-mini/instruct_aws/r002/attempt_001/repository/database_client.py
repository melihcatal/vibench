import os
from functools import lru_cache

import boto3


DEFAULT_TABLE_NAME = os.getenv("AWS_DYNAMODB_TABLE_NAME", "documents")
DEFAULT_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


@lru_cache(maxsize=1)
def dynamodb_resource():
    return boto3.resource("dynamodb", region_name=DEFAULT_REGION)


@lru_cache(maxsize=1)
def dynamodb_table(table_name: str = DEFAULT_TABLE_NAME):
    return dynamodb_resource().Table(table_name)


def document_key(identifier):
    return {"document_id": str(identifier)}


def table_name_from_env():
    return DEFAULT_TABLE_NAME
