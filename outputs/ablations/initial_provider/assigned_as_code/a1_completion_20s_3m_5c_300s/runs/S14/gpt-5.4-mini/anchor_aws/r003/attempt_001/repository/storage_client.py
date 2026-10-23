import os

import boto3


def storage_config(config=None):
    merged = {}
    merged.update({
        "region": os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "bucket": os.getenv("S3_BUCKET"),
        "prefix": os.getenv("S3_PREFIX", ""),
    })
    if config:
        merged.update(config)
    return merged


def storage_client(config=None):
    cfg = storage_config(config)
    return boto3.client("s3", region_name=cfg.get("region"))
