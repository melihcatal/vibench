import os

import boto3


def load_config(config=None):
    config = dict(config or {})
    if "region" not in config:
        config["region"] = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    if "table_name" not in config:
        config["table_name"] = os.getenv("DYNAMODB_TABLE_NAME")
    if "bucket_name" not in config:
        config["bucket_name"] = os.getenv("S3_BUCKET_NAME")
    if "key_field" not in config:
        config["key_field"] = os.getenv("DYNAMODB_KEY_FIELD", "id")
    if "sort_field" not in config:
        config["sort_field"] = os.getenv("DYNAMODB_SORT_FIELD")
    return config


def dynamodb_table(config):
    cfg = load_config(config)
    return boto3.resource("dynamodb", region_name=cfg.get("region")).Table(cfg["table_name"])


def s3_client(config=None):
    cfg = load_config(config)
    return boto3.client("s3", region_name=cfg.get("region"))
