import os

import boto3


def load_observability_config(config=None):
    base = dict(config or {})
    if not base.get("region"):
        base["region"] = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    return base


def cloudwatch_client(config=None):
    config = load_observability_config(config)
    return boto3.client("cloudwatch", region_name=config.get("region"))


def s3_client(config=None):
    config = load_observability_config(config)
    return boto3.client("s3", region_name=config.get("region"))
