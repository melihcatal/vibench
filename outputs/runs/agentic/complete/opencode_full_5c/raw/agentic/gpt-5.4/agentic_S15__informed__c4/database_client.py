from __future__ import annotations

import os
from typing import Any

import boto3
from boto3.dynamodb.conditions import Attr, Key

from database_models import prepare_document


def get_table_name() -> str:
    return os.environ.get("DYNAMODB_TABLE_NAME", "documents")


def get_partition_key_name() -> str:
    return os.environ.get("DYNAMODB_PARTITION_KEY_NAME", "id")


def get_dynamodb_resource():
    region = (
        os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or "us-east-1"
    )
    endpoint_url = os.environ.get("DYNAMODB_ENDPOINT_URL")
    return boto3.resource("dynamodb", region_name=region, endpoint_url=endpoint_url)


def get_documents_table():
    return get_dynamodb_resource().Table(get_table_name())


def build_key(document_id: str, partition_value: str | None = None) -> dict[str, Any]:
    key_name = get_partition_key_name()
    key: dict[str, Any] = {
        key_name: document_id if key_name == "id" else partition_value or document_id
    }
    if key_name != "id":
        key["id"] = document_id
    return prepare_document(key)


def build_partition_query(
    field_name: str, field_value: Any, index_name: str | None = None
) -> dict[str, Any]:
    value = prepare_document({"value": field_value})["value"]
    if index_name:
        return {
            "IndexName": index_name,
            "KeyConditionExpression": Key(field_name).eq(value),
        }
    return {
        "FilterExpression": Attr(field_name).eq(value),
    }
