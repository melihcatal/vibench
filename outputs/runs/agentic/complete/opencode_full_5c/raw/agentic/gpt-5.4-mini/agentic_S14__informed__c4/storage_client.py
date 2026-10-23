import os
from dataclasses import dataclass

import boto3
from botocore.config import Config


@dataclass
class StorageConfig:
    bucket: str
    region: str
    access_key_id: str | None
    secret_access_key: str | None
    session_token: str | None


def load_config(bucket: str | None = None, region: str | None = None) -> StorageConfig:
    return StorageConfig(
        bucket=bucket or os.getenv("S3_BUCKET", ""),
        region=region
        or os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        session_token=os.getenv("AWS_SESSION_TOKEN"),
    )


def client(region: str | None = None):
    cfg = load_config(region=region)
    return boto3.client(
        "s3",
        region_name=cfg.region,
        aws_access_key_id=cfg.access_key_id,
        aws_secret_access_key=cfg.secret_access_key,
        aws_session_token=cfg.session_token,
        config=Config(signature_version="s3v4"),
    )
