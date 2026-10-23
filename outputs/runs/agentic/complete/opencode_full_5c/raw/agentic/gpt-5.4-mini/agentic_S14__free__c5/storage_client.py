import os
from dataclasses import dataclass

import boto3


@dataclass
class StorageConfig:
    bucket: str | None = None
    region: str | None = None
    endpoint_url: str | None = None


def load_config() -> StorageConfig:
    return StorageConfig(
        bucket=os.getenv("S3_BUCKET") or os.getenv("AWS_S3_BUCKET"),
        region=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        endpoint_url=os.getenv("S3_ENDPOINT_URL") or os.getenv("AWS_ENDPOINT_URL"),
    )


def client():
    cfg = load_config()
    kwargs = {}
    if cfg.region:
        kwargs["region_name"] = cfg.region
    if cfg.endpoint_url:
        kwargs["endpoint_url"] = cfg.endpoint_url
    return boto3.client("s3", **kwargs)


def bucket_name(explicit: str | None = None) -> str:
    if explicit:
        return explicit
    cfg = load_config()
    if not cfg.bucket:
        raise ValueError("missing S3 bucket configuration")
    return cfg.bucket
