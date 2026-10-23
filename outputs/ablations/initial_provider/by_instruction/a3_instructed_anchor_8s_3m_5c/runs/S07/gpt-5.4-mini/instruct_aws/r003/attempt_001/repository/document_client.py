import os
from functools import lru_cache

import boto3


def _region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


@lru_cache(maxsize=1)
def textract_client():
    return boto3.client("textract", region_name=_region())


def s3_object_reference(bucket: str, key: str, version: str | None = None):
    ref = {"S3Object": {"Bucket": bucket, "Name": key}}
    if version:
        ref["S3Object"]["Version"] = version
    return ref


def load_document_input(bucket: str | None = None, key: str | None = None, version: str | None = None):
    bucket = bucket or os.getenv("DOCUMENT_BUCKET", "")
    key = key or os.getenv("DOCUMENT_KEY", "")
    if not bucket or not key:
        raise ValueError("bucket and key are required")
    return bucket, key, version
