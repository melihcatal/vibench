from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional

import boto3
from botocore.client import Config
from botocore.exceptions import BotoCoreError, ClientError


@dataclass(slots=True)
class StorageConfig:
    region_name: Optional[str] = None
    endpoint_url: Optional[str] = None
    signature_version: str = "s3v4"


def load_storage_config() -> StorageConfig:
    return StorageConfig(
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),
        signature_version=os.getenv("S3_SIGNATURE_VERSION", "s3v4"),
    )


def create_storage_client(service_name: str = "s3"):
    cfg = load_storage_config()
    return boto3.client(
        service_name,
        region_name=cfg.region_name,
        endpoint_url=cfg.endpoint_url,
        config=Config(signature_version=cfg.signature_version),
    )


def ensure_client_error(result: Any) -> Any:
    if isinstance(result, (BotoCoreError, ClientError)):
        raise result
    return result


S3 = "s3"
