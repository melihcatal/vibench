import os
from functools import lru_cache
from typing import Optional

from boto3.session import Session
from botocore.client import Config

from storage_models import normalize_object_key, normalize_prefix


@lru_cache(maxsize=1)
def get_s3_client():
    return Session().client(
        's3',
        region_name=os.getenv('AWS_REGION') or os.getenv('AWS_DEFAULT_REGION'),
        config=Config(signature_version='s3v4'),
    )


def get_bucket_name() -> str:
    bucket = os.getenv('S3_BUCKET') or os.getenv('AWS_S3_BUCKET')
    if not bucket:
        raise ValueError('S3_BUCKET or AWS_S3_BUCKET is required')
    return bucket


def make_object_key(key: str) -> str:
    return normalize_object_key(key)


def make_prefix(prefix: str) -> str:
    return normalize_prefix(prefix)


def optional_content_type(value: Optional[str]) -> Optional[str]:
    return value or None
