import os
from functools import lru_cache

import boto3


def _env(name, default=None):
    value = os.getenv(name, default)
    return value


@lru_cache(maxsize=1)
def get_dynamodb_resource():
    return boto3.resource(
        "dynamodb",
        aws_access_key_id=_env("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=_env("AWS_SECRET_ACCESS_KEY"),
        region_name=_env("AWS_REGION", _env("AWS_DEFAULT_REGION", "us-east-1")),
    )


@lru_cache(maxsize=1)
def get_table(table_name=None):
    table_name = table_name or _env("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise ValueError("DYNAMODB_TABLE_NAME is required")
    return get_dynamodb_resource().Table(table_name)


def get_primary_key_name():
    return _env("DYNAMODB_PRIMARY_KEY", "id")


def get_partition_key_name():
    return _env("DYNAMODB_PARTITION_KEY", "partition")


def get_version_key_name():
    return _env("DYNAMODB_VERSION_KEY", "version")
