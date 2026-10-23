import os
from typing import Any, Dict

import boto3


def get_table_name() -> str:
    name = os.getenv("DYNAMODB_TABLE_NAME")
    if not name:
        raise RuntimeError("DYNAMODB_TABLE_NAME is required")
    return name


def get_dynamodb_resource():
    region = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
    return boto3.resource("dynamodb", region_name=region)


def get_table():
    return get_dynamodb_resource().Table(get_table_name())


def make_key(document_id: str, id_field: str = "id") -> Dict[str, Any]:
    return {id_field: document_id}
