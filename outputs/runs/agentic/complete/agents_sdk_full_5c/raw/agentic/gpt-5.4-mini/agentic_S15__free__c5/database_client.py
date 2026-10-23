from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

DEFAULT_TABLE_NAME = os.getenv("DOCUMENT_TABLE_NAME", "managed-document-store")
DEFAULT_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
DEFAULT_ENDPOINT_URL = os.getenv("DYNAMODB_ENDPOINT_URL")


@lru_cache(maxsize=1)
def get_dynamodb_resource():
    session = boto3.session.Session(region_name=DEFAULT_REGION)
    return session.resource(
        "dynamodb",
        region_name=DEFAULT_REGION,
        endpoint_url=DEFAULT_ENDPOINT_URL,
        config=Config(retries={"max_attempts": 5, "mode": "standard"}),
    )


@lru_cache(maxsize=1)
def get_table(table_name: Optional[str] = None):
    resource = get_dynamodb_resource()
    return resource.Table(table_name or DEFAULT_TABLE_NAME)


def get_dynamodb_client():
    session = boto3.session.Session(region_name=DEFAULT_REGION)
    return session.client(
        "dynamodb",
        region_name=DEFAULT_REGION,
        endpoint_url=DEFAULT_ENDPOINT_URL,
        config=Config(retries={"max_attempts": 5, "mode": "standard"}),
    )


def service_error_payload(exc: Exception) -> Dict[str, Any]:
    if isinstance(exc, ClientError):
        err = exc.response.get("Error", {})
        return {
            "error_type": err.get("Code", "ClientError"),
            "message": err.get("Message", str(exc)),
        }
    if isinstance(exc, BotoCoreError):
        return {"error_type": exc.__class__.__name__, "message": str(exc)}
    return {"error_type": exc.__class__.__name__, "message": str(exc)}
