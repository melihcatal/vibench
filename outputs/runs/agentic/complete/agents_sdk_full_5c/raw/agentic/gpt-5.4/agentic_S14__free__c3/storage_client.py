from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import boto3
from botocore.client import BaseClient
from botocore.config import Config


@dataclass(slots=True)
class StorageConfig:
    bucket: str
    region: str
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_session_token: Optional[str] = None
    endpoint_url: Optional[str] = None



def load_storage_config(bucket: Optional[str] = None) -> StorageConfig:
    resolved_bucket = bucket or os.environ["S3_BUCKET"]
    return StorageConfig(
        bucket=resolved_bucket,
        region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        endpoint_url=os.getenv("AWS_S3_ENDPOINT_URL"),
    )



def create_s3_client(config: Optional[StorageConfig] = None) -> BaseClient:
    cfg = config or load_storage_config()
    return boto3.client(
        "s3",
        region_name=cfg.region,
        aws_access_key_id=cfg.aws_access_key_id,
        aws_secret_access_key=cfg.aws_secret_access_key,
        aws_session_token=cfg.aws_session_token,
        endpoint_url=cfg.endpoint_url,
        config=Config(signature_version="s3v4"),
    )



def create_textract_client(region: Optional[str] = None) -> BaseClient:
    resolved_region = region or os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
    return boto3.client("textract", region_name=resolved_region)



def create_translate_client(region: Optional[str] = None) -> BaseClient:
    resolved_region = region or os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
    return boto3.client("translate", region_name=resolved_region)
