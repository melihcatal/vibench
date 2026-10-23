import os
from functools import lru_cache

import boto3


def _env(name, default=None):
    value = os.getenv(name)
    return default if value is None or value == "" else value


def database_config():
    return {
        "table_name": _env("DYNAMODB_TABLE_NAME", "managed-document-store"),
        "region_name": _env("AWS_REGION", _env("AWS_DEFAULT_REGION", "us-east-1")),
        "endpoint_url": _env("DYNAMODB_ENDPOINT_URL"),
    }


@lru_cache(maxsize=1)
def get_dynamodb_resource():
    config = database_config()
    kwargs = {"region_name": config["region_name"]}
    if config["endpoint_url"]:
        kwargs["endpoint_url"] = config["endpoint_url"]
    return boto3.resource("dynamodb", **kwargs)


def get_table(table_name=None):
    config = database_config()
    return get_dynamodb_resource().Table(table_name or config["table_name"])


def table_name():
    return database_config()["table_name"]
