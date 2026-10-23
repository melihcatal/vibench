import os
import boto3


def get_storage_config(config=None):
    config = dict(config or {})
    if "bucket" not in config:
        config["bucket"] = os.environ.get("S3_BUCKET") or os.environ.get("BUCKET")
    if "region" not in config:
        config["region"] = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    return config


def get_s3_client(config=None):
    config = get_storage_config(config)
    return boto3.client("s3", region_name=config.get("region"))
