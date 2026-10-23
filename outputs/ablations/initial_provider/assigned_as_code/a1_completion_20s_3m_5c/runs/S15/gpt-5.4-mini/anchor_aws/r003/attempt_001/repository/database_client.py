import os

import boto3


def load_config(config=None):
    config = config or {}
    return {
        "region": config.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
        "table_name": config.get("table_name") or os.environ["DYNAMODB_TABLE_NAME"],
        "key_field": config.get("key_field") or os.environ.get("DYNAMODB_KEY_FIELD", "id"),
        "version_field": config.get("version_field") or os.environ.get("DYNAMODB_VERSION_FIELD", "version"),
    }


def get_table(config=None):
    cfg = load_config(config)
    return boto3.resource("dynamodb", region_name=cfg["region"]).Table(cfg["table_name"])
