from __future__ import annotations

import os
from typing import BinaryIO, Any

import boto3
from botocore.client import BaseClient
from botocore.config import Config


def get_s3_client() -> BaseClient:
    region_name = (
        os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    )
    endpoint_url = os.getenv("S3_ENDPOINT_URL")
    session = boto3.session.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        region_name=region_name,
    )
    return session.client(
        "s3",
        endpoint_url=endpoint_url,
        config=Config(signature_version="s3v4"),
    )


def get_textract_client() -> BaseClient:
    region_name = (
        os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    )
    session = boto3.session.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        region_name=region_name,
    )
    return session.client("textract")


def read_binary_payload(data: bytes | BinaryIO) -> bytes:
    if isinstance(data, bytes):
        return data
    chunk = data.read()
    if isinstance(chunk, str):
        return chunk.encode("utf-8")
    return chunk


def build_s3_uri(bucket_name: str, object_name: str) -> str:
    return f"s3://{bucket_name}/{object_name}"


def merge_document_text(pages: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for page in pages:
        for line in page.get("lines", []):
            text = line.get("text")
            if text:
                lines.append(text)
    return "\n".join(lines)
