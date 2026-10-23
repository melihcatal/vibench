import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3
from botocore.client import Config
from botocore.exceptions import BotoCoreError, ClientError

S3_ENDPOINT_ENV = "S3_ENDPOINT_URL"
S3_REGION_ENV = "AWS_REGION"
S3_PROFILE_ENV = "AWS_PROFILE"
S3_SIGNATURE_ENV = "S3_SIGNATURE_VERSION"


@dataclass(frozen=True)
class StorageConfig:
    endpoint_url: Optional[str]
    region_name: str
    profile_name: Optional[str]
    signature_version: str


def load_storage_config() -> StorageConfig:
    return StorageConfig(
        endpoint_url=os.getenv(S3_ENDPOINT_ENV),
        region_name=os.getenv(S3_REGION_ENV, "us-east-1"),
        profile_name=os.getenv(S3_PROFILE_ENV),
        signature_version=os.getenv(S3_SIGNATURE_ENV, "s3v4"),
    )


@lru_cache(maxsize=1)
def get_s3_resource():
    cfg = load_storage_config()
    session = boto3.Session(profile_name=cfg.profile_name) if cfg.profile_name else boto3.Session()
    return session.resource(
        "s3",
        endpoint_url=cfg.endpoint_url,
        region_name=cfg.region_name,
        config=Config(signature_version=cfg.signature_version),
    )


@lru_cache(maxsize=1)
def get_s3_client():
    cfg = load_storage_config()
    session = boto3.Session(profile_name=cfg.profile_name) if cfg.profile_name else boto3.Session()
    return session.client(
        "s3",
        endpoint_url=cfg.endpoint_url,
        region_name=cfg.region_name,
        config=Config(signature_version=cfg.signature_version),
    )


def get_bucket(bucket_name: str):
    return get_s3_resource().Bucket(bucket_name)


def raise_storage_error(exc: Exception) -> RuntimeError:
    if isinstance(exc, (BotoCoreError, ClientError)):
        return RuntimeError(f"Amazon S3 operation failed: {exc}")
    return RuntimeError(str(exc))
