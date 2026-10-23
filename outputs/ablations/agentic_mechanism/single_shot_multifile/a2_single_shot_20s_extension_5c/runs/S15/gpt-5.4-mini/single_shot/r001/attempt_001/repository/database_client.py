import os
from functools import lru_cache
from typing import Optional

import boto3

DEFAULT_TABLE_NAME = os.getenv("DOCUMENT_TABLE_NAME", "ManagedDocumentStore")
DEFAULT_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


@lru_cache(maxsize=1)
def get_boto3_session() -> boto3.session.Session:
    return boto3.Session(region_name=DEFAULT_REGION)


@lru_cache(maxsize=1)
def get_dynamodb_resource():
    return get_boto3_session().resource("dynamodb")


@lru_cache(maxsize=1)
def get_document_table(table_name: Optional[str] = None):
    return get_dynamodb_resource().Table(table_name or DEFAULT_TABLE_NAME)


def get_table_name() -> str:
    return DEFAULT_TABLE_NAME