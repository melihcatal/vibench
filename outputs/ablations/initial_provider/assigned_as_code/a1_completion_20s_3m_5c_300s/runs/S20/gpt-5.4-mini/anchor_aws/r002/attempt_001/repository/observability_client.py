import os

import boto3


def load_observability_config(config=None):
    config = dict(config or {})
    if "region" not in config:
        config["region"] = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    if "log_group" not in config:
        config["log_group"] = os.getenv("CLOUDWATCH_LOG_GROUP")
    if "log_stream" not in config:
        config["log_stream"] = os.getenv("CLOUDWATCH_LOG_STREAM")
    return config


def build_cloudwatch_logs_client(config=None):
    config = load_observability_config(config)
    return boto3.client("logs", region_name=config.get("region"))
