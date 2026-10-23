import os
from dataclasses import dataclass
from typing import Optional

import boto3
from botocore.config import Config


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in ("", None) else default


@dataclass(frozen=True)
class StorageConfig:
    bucket: Optional[str] = _env("AWS_S3_BUCKET")
    region: Optional[str] = _env("AWS_REGION", _env("AWS_DEFAULT_REGION"))
    endpoint_url: Optional[str] = _env("AWS_S3_ENDPOINT_URL")
    profile: Optional[str] = _env("AWS_PROFILE")
    prefix: str = _env("AWS_S3_PREFIX", "") or ""
    signature_version: str = _env("AWS_S3_SIGNATURE_VERSION", "s3v4") or "s3v4"


def get_s3_client(config: Optional[StorageConfig] = None):
    config = config or StorageConfig()
    session = boto3.session.Session(profile_name=config.profile, region_name=config.region)
    return session.client(
        "s3",
        endpoint_url=config.endpoint_url,
        config=Config(signature_version=config.signature_version),
    )


def get_object_key(name: str, prefix: Optional[str] = None) -> str:
    prefix = StorageConfig().prefix if prefix is None else prefix
    prefix = prefix.strip("/")
    name = name.lstrip("/")
    return f"{prefix}/{name}" if prefix else name


def get_bucket_name(bucket: Optional[str] = None) -> str:
    resolved = bucket or StorageConfig().bucket
    if not resolved:
        raise ValueError("AWS_S3_BUCKET is required")
    return resolved


def build_s3_uri(bucket: Optional[str], key: str) -> str:
    return f"s3://{get_bucket_name(bucket)}/{key.lstrip('/')}"


def create_presigned_download_url(
    bucket: Optional[str],
    key: str,
    expires_in_seconds: int = 3600,
    config: Optional[StorageConfig] = None,
) -> str:
    cfg = config or StorageConfig()
    client = get_s3_client(cfg)
    return client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": get_bucket_name(bucket), "Key": key},
        ExpiresIn=expires_in_seconds,
    )


def create_presigned_upload_url(
    bucket: Optional[str],
    key: str,
    expires_in_seconds: int = 3600,
    content_type: Optional[str] = None,
    config: Optional[StorageConfig] = None,
) -> str:
    cfg = config or StorageConfig()
    client = get_s3_client(cfg)
    params = {"Bucket": get_bucket_name(bucket), "Key": key}
    if content_type:
        params["ContentType"] = content_type
    return client.generate_presigned_url(
        ClientMethod="put_object",
        Params=params,
        ExpiresIn=expires_in_seconds,
    )
