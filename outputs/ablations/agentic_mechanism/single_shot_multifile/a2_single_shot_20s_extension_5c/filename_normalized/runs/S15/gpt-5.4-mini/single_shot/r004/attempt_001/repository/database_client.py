import os
from functools import lru_cache
from typing import Any

import boto3


@lru_cache(maxsize=1)
def get_dynamodb_resource():
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
    return boto3.resource("dynamodb", region_name=region)


def get_table():
    table_name = os.environ["DYNAMODB_TABLE"]
    return get_dynamodb_resource().Table(table_name)
