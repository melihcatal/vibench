"""
Local configuration and client helper utilities for Amazon DynamoDB.

Provides client initialization, table resource access, and common
configuration helpers for interacting with the managed NoSQL document store.
"""

import os
import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError, BotoCoreError


TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME", "document-store")
AWS_REGION = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))


def get_dynamodb_client():
    """Return a boto3 DynamoDB client using environment credentials."""
    return boto3.client(
        "dynamodb",
        region_name=AWS_REGION,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )


def get_dynamodb_resource():
    """Return a boto3 DynamoDB resource for higher-level table operations."""
    return boto3.resource(
        "dynamodb",
        region_name=AWS_REGION,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )


def get_table(table_name=None):
    """Return a Table resource for the configured DynamoDB table."""
    resource = get_dynamodb_resource()
    target = table_name or TABLE_NAME
    return resource.Table(target)


def build_key_condition(partition_key, sort_key=None):
    """Build a Key condition expression for DynamoDB queries."""
    if sort_key:
        return Key(partition_key).eq(sort_key["pk"]) & Key(sort_key["sk"]).eq(sort_key["sk_value"])
    return Key(partition_key)


def build_attribute_filter(field, value):
    """Build an Attr filter for filtering on non-key attributes."""
    return Attr(field).eq(value)


def handle_dynamodb_error(operation, error):
    """Translate DynamoDB ClientError into a structured response dict."""
    if isinstance(error, ClientError):
        code = error.response["Error"]["Code"]
        message = error.response["Error"]["Message"]
        return {
            "success": False,
            "operation": operation,
            "error_code": code,
            "message": message,
        }
    if isinstance(error, BotoCoreError):
        return {
            "success": False,
            "operation": operation,
            "error_code": "BotoCoreError",
            "message": str(error),
        }
    return {
        "success": False,
        "operation": operation,
        "error_code": "UnknownError",
        "message": str(error),
    }


def normalize_dynamodb_item(item):
    """Convert a DynamoDB response item into a plain Python dict.

    DynamoDB returns values wrapped in type descriptors (S, N, B, etc.).
    This helper unwraps them for easier consumption by downstream services.
    """
    if item is None:
        return None

    def _unwrap(value):
        if isinstance(value, dict):
            if "S" in value:
                return value["S"]
            if "N" in value:
                numeric = value["N"]
                try:
                    return int(numeric)
                except ValueError:
                    return float(numeric)
            if "B" in value:
                return value["B"]
            if "BOOL" in value:
                return value["BOOL"]
            if "NULL" in value:
                return None
            if "L" in value:
                return [_unwrap(v) for v in value["L"]]
            if "M" in value:
                return {k: _unwrap(v) for k, v in value["M"].items()}
            if "SS" in value:
                return set(value["SS"])
            if "NS" in value:
                return set(int(n) if "." not in n else float(n) for n in value["NS"])
            if "BS" in value:
                return set(value["BS"])
            return value
        return value

    return {k: _unwrap(v) for k, v in item.items()}
