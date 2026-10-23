import os
from functools import lru_cache

import boto3
from botocore.config import Config


def _env(name, default=None):
    value = os.getenv(name, default)
    return value


def database_config():
    return {
        "aws_region": _env("AWS_REGION", _env("AWS_DEFAULT_REGION", "us-east-1")),
        "aws_access_key_id": _env("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": _env("AWS_SECRET_ACCESS_KEY"),
        "aws_session_token": _env("AWS_SESSION_TOKEN"),
        "dynamodb_table_name": _env("DYNAMODB_TABLE_NAME", "documents"),
        "document_primary_key": _env("DOCUMENT_PRIMARY_KEY", "document_id"),
        "document_partition_key": _env("DOCUMENT_PARTITION_KEY", "category"),
        "aws_s3_bucket": _env("AWS_S3_BUCKET", "document-archives"),
    }


@lru_cache(maxsize=1)
def dynamodb_resource():
    cfg = database_config()
    return boto3.resource(
        "dynamodb",
        region_name=cfg["aws_region"],
        aws_access_key_id=cfg["aws_access_key_id"],
        aws_secret_access_key=cfg["aws_secret_access_key"],
        aws_session_token=cfg["aws_session_token"],
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


@lru_cache(maxsize=1)
def s3_client():
    cfg = database_config()
    return boto3.client(
        "s3",
        region_name=cfg["aws_region"],
        aws_access_key_id=cfg["aws_access_key_id"],
        aws_secret_access_key=cfg["aws_secret_access_key"],
        aws_session_token=cfg["aws_session_token"],
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


def document_table():
    cfg = database_config()
    return dynamodb_resource().Table(cfg["dynamodb_table_name"])
