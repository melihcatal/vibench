import os
from functools import lru_cache

import boto3
from botocore.client import Config


def get_storage_config() -> dict:
    return {
        "region_name": os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "endpoint_url": os.getenv("S3_ENDPOINT_URL"),
        "signature_version": os.getenv("S3_SIGNATURE_VERSION", "s3v4"),
    }


@lru_cache(maxsize=1)
def get_s3_client():
    config = get_storage_config()
    kwargs = {k: v for k, v in config.items() if v}
    return boto3.client("s3", config=Config(signature_version=kwargs.pop("signature_version", "s3v4")), **kwargs)
