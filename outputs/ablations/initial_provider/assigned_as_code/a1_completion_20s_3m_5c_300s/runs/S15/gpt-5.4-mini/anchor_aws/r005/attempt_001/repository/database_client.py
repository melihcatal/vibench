import os

import boto3


def load_database_config(config=None):
    config = config or {}
    return {
        "region": config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "table_name": config.get("table_name") or os.getenv("DYNAMODB_TABLE_NAME"),
        "bucket_name": config.get("bucket_name") or os.getenv("S3_BUCKET_NAME"),
        "key_field": config.get("key_field", "id"),
    }


def get_dynamodb_table(config=None):
    config = load_database_config(config)
    return boto3.resource("dynamodb", region_name=config["region"]).Table(config["table_name"])


def get_s3_client(config=None):
    config = load_database_config(config)
    return boto3.client("s3", region_name=config["region"]), config["bucket_name"]
