from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3
from botocore.client import Config
from botocore.exceptions import BotoCoreError, ClientError


@dataclass(frozen=True)
class StorageConfig:
    bucket: str
    region_name: str
    endpoint_url: Optional[str] = None
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    session_token: Optional[str] = None


@lru_cache(maxsize=1)
def load_storage_config() -> StorageConfig:
    bucket = os.environ.get("S3_BUCKET") or os.environ.get("AWS_S3_BUCKET")
    if not bucket:
        raise ValueError("S3_BUCKET or AWS_S3_BUCKET must be set")
    return StorageConfig(
        bucket=bucket,
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
        access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        session_token=os.environ.get("AWS_SESSION_TOKEN"),
    )


def create_s3_client():
    cfg = load_storage_config()
    return boto3.client(
        "s3",
        region_name=cfg.region_name,
        endpoint_url=cfg.endpoint_url,
        aws_access_key_id=cfg.access_key_id,
        aws_secret_access_key=cfg.secret_access_key,
        aws_session_token=cfg.session_token,
        config=Config(signature_version=os.environ.get("S3_SIGNATURE_VERSION", "s3v4")),
    )


def normalize_boto_error(exc: Exception) -> dict:
    if isinstance(exc, ClientError):
        err = exc.response.get("Error", {})
        return {"type": "ClientError", "code": err.get("Code"), "message": err.get("Message")}
    if isinstance(exc, BotoCoreError):
        return {"type": exc.__class__.__name__, "message": str(exc)}
    return {"type": exc.__class__.__name__, "message": str(exc)}
