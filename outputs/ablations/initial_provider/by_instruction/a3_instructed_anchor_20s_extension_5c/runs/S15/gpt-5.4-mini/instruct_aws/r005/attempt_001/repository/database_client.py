import os
from functools import lru_cache

import boto3


def table_name():
    return os.getenv("DYNAMODB_TABLE_NAME", "managed_nosql_documents")


def region_name():
    return os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


@lru_cache(maxsize=1)
def dynamodb_resource():
    return boto3.resource("dynamodb", region_name=region_name())


@lru_cache(maxsize=1)
def dynamodb_table():
    return dynamodb_resource().Table(table_name())


def client_config():
    return {"service": "aws_dynamodb", "region": region_name(), "table": table_name()}
