import os

import boto3


def load_storage_config(config=None):
    config = dict(config or {})
    if "bucket" not in config:
        config["bucket"] = os.environ["STORAGE_BUCKET"]
    if "region" not in config:
        config["region"] = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    return config


def get_s3_client(config=None):
    config = load_storage_config(config)
    return boto3.client("s3", region_name=config.get("region"))
