import os

import boto3


def get_config(config=None):
    config = config or {}
    merged = {
        "region": config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "table_name": config.get("table_name") or os.getenv("DYNAMODB_TABLE_NAME"),
        "bucket_name": config.get("bucket_name") or os.getenv("S3_BUCKET_NAME"),
        "key_field": config.get("key_field", "id"),
        "version_field": config.get("version_field", "version"),
    }
    if not merged["table_name"]:
        raise ValueError("table_name is required")
    return merged


def get_table(config=None):
    cfg = get_config(config)
    return boto3.resource("dynamodb", region_name=cfg["region"]).Table(cfg["table_name"]), cfg


def get_s3_client(config=None):
    cfg = get_config(config)
    return boto3.client("s3", region_name=cfg["region"]), cfg
