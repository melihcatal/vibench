import os
from dataclasses import dataclass

import boto3


@dataclass
class StorageConfig:
    bucket_name: str
    region_name: str | None = None


def load_storage_config() -> StorageConfig:
    bucket_name = os.environ.get("S3_BUCKET_NAME", "")
    region_name = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    return StorageConfig(bucket_name=bucket_name, region_name=region_name)


def get_s3_client():
    config = load_storage_config()
    session = boto3.session.Session(region_name=config.region_name)
    return session.client("s3")


def get_bucket_name() -> str:
    return load_storage_config().bucket_name
