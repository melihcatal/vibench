from __future__ import annotations

import os
from typing import BinaryIO

import boto3
from botocore.client import BaseClient


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_s3_client() -> BaseClient:
    session = boto3.session.Session(region_name=get_aws_region())
    endpoint_url = os.getenv("AWS_S3_ENDPOINT_URL")
    return session.client("s3", endpoint_url=endpoint_url)


def get_textract_client() -> BaseClient:
    session = boto3.session.Session(region_name=get_aws_region())
    return session.client("textract")


def read_upload_bytes(
    body: bytes | bytearray | BinaryIO | None, file_path: str | None
) -> bytes:
    if body is not None:
        if hasattr(body, "read"):
            return body.read()
        return bytes(body)
    if not file_path:
        raise ValueError("Either body or file_path must be provided")
    with open(file_path, "rb") as handle:
        return handle.read()


def default_bucket() -> str | None:
    return os.getenv("AWS_S3_BUCKET")


def openai_api_key() -> str:
    value = os.getenv("OPENAI_API_KEY")
    if not value:
        raise ValueError("OPENAI_API_KEY is required")
    return value


def google_translate_api_key() -> str:
    value = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    if not value:
        raise ValueError("GOOGLE_TRANSLATE_API_KEY is required")
    return value
