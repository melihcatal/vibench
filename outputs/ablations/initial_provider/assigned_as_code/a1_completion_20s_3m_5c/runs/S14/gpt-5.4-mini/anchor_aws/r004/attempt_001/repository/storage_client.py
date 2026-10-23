import os

import boto3


def load_storage_config(config=None):
    config = config or {}
    return {
        "bucket": config.get("bucket") or os.environ["S3_BUCKET"],
        "region": config.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
        "expires_in": int(config.get("expires_in", 3600)),
    }


def get_s3_client(config=None):
    config = load_storage_config(config)
    return boto3.client("s3", region_name=config.get("region"))


def get_bucket_name(config=None):
    return load_storage_config(config)["bucket"]
