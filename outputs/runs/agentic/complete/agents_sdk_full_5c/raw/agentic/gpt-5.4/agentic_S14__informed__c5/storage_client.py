from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.client import BaseClient
from botocore.config import Config

DEFAULT_S3_SIGNATURE_VERSION = "s3v4"


class StorageConfigError(ValueError):
    pass


def get_s3_client(region_name: Optional[str] = None) -> BaseClient:
    region = region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    endpoint_url = os.getenv("AWS_S3_ENDPOINT_URL")
    session = boto3.session.Session(region_name=region)
    return session.client(
        "s3",
        endpoint_url=endpoint_url,
        config=Config(signature_version=DEFAULT_S3_SIGNATURE_VERSION),
    )


def get_textract_client(region_name: Optional[str] = None) -> BaseClient:
    region = region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    return boto3.session.Session(region_name=region).client("textract")


def require_bucket(bucket: Optional[str] = None) -> str:
    resolved = bucket or os.getenv("S3_BUCKET")
    if not resolved:
        raise StorageConfigError("Missing S3 bucket. Provide bucket argument or set S3_BUCKET.")
    return resolved


def read_bytes(file_path: Optional[str] = None, data: Optional[bytes] = None) -> bytes:
    if data is not None:
        return data
    if not file_path:
        raise ValueError("Provide either file_path or data.")
    with open(file_path, "rb") as handle:
        return handle.read()
