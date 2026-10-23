import os
from functools import lru_cache
from pathlib import Path
from typing import Any, BinaryIO, Union

import boto3
from botocore.client import BaseClient

AWS_REGION_ENV = 'AWS_REGION'
S3_BUCKET_ENV = 'S3_BUCKET'
S3_ENDPOINT_ENV = 'S3_ENDPOINT_URL'


def get_bucket_name() -> str:
    bucket = os.environ.get(S3_BUCKET_ENV)
    if not bucket:
        raise ValueError('S3_BUCKET is required')
    return bucket


@lru_cache(maxsize=1)
def get_s3_client() -> BaseClient:
    kwargs: dict[str, Any] = {}
    endpoint = os.environ.get(S3_ENDPOINT_ENV)
    region = os.environ.get(AWS_REGION_ENV)
    if endpoint:
        kwargs['endpoint_url'] = endpoint
    if region:
        kwargs['region_name'] = region
    return boto3.client('s3', **kwargs)


def read_bytes(source: Union[str, bytes, bytearray, BinaryIO]) -> bytes:
    if isinstance(source, bytes):
        return source
    if isinstance(source, bytearray):
        return bytes(source)
    if isinstance(source, str):
        return Path(source).read_bytes()
    return source.read()


def object_key_from_path(source: Union[str, bytes, bytearray, BinaryIO]) -> str:
    if isinstance(source, str):
        return Path(source).name
    raise ValueError('object_key is required')
