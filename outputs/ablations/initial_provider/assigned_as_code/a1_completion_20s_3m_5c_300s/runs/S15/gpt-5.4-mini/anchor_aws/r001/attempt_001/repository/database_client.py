import os

import boto3


def load_config(config=None):
    config = config or {}
    return {
        "region": config.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
        "table_name": config.get("table_name") or os.environ["DYNAMODB_TABLE_NAME"],
        "key_field": config.get("key_field", "id"),
        "object_bucket": config.get("object_bucket") or os.environ.get("S3_EXPORT_BUCKET"),
    }


def dynamodb_resource(config=None):
    cfg = load_config(config)
    return boto3.resource("dynamodb", region_name=cfg["region"])


def dynamodb_table(config=None):
    cfg = load_config(config)
    return dynamodb_resource(cfg).Table(cfg["table_name"])


def s3_client(config=None):
    cfg = load_config(config)
    return boto3.client("s3", region_name=cfg["region"])
