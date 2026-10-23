import os
from dataclasses import dataclass
from typing import Optional

import boto3
from botocore.config import Config


@dataclass(frozen=True)
class StorageConfig:
    aws_region: str
    aws_access_key_id: Optional[str]
    aws_secret_access_key: Optional[str]
    aws_session_token: Optional[str]
    s3_endpoint_url: Optional[str]


def get_storage_config() -> StorageConfig:
    return StorageConfig(
        aws_region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        s3_endpoint_url=os.getenv("S3_ENDPOINT_URL"),
    )


def create_s3_client(config: Optional[StorageConfig] = None):
    cfg = config or get_storage_config()
    session = boto3.session.Session(
        aws_access_key_id=cfg.aws_access_key_id,
        aws_secret_access_key=cfg.aws_secret_access_key,
        aws_session_token=cfg.aws_session_token,
        region_name=cfg.aws_region,
    )
    return session.client("s3", endpoint_url=cfg.s3_endpoint_url, config=Config(signature_version="s3v4"))
