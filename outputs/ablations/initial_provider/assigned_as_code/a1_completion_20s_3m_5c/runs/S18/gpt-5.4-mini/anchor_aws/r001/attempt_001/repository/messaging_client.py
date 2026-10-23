import os

import boto3


def load_config(overrides=None):
    overrides = overrides or {}
    config = {
        "region": overrides.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
    }
    config.update(overrides)
    return config


def sns_client(config=None):
    config = load_config(config)
    return boto3.client("sns", region_name=config.get("region"))


def sqs_client(config=None):
    config = load_config(config)
    return boto3.client("sqs", region_name=config.get("region"))
