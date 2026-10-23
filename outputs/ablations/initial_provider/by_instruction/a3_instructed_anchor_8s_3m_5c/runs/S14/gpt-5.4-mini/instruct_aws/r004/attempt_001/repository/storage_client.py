import os
from functools import lru_cache

import boto3
from botocore.client import Config


def _env(name, default=None):
    value = os.environ.get(name, default)
    return value


def get_region():
    return _env("AWS_REGION") or _env("AWS_DEFAULT_REGION") or "us-east-1"


def get_bucket_name():
    return _env("AWS_STORAGE_BUCKET") or _env("S3_BUCKET") or _env("BUCKET_NAME")


@lru_cache(maxsize=1)
def get_s3_client():
    return boto3.client("s3", region_name=get_region(), config=Config(signature_version="s3v4"))


def normalize_body(payload):
    if payload is None:
        return b""
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, bytearray):
        return bytes(payload)
    if isinstance(payload, str):
        return payload.encode("utf-8")
    if hasattr(payload, "read"):
        data = payload.read()
        if isinstance(data, str):
            return data.encode("utf-8")
        return data
    raise TypeError("Unsupported payload type")
