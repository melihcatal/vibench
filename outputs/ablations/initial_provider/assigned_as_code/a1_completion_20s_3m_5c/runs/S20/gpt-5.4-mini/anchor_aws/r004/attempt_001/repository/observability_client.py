import os

import boto3


def load_config(config=None):
    config = config or {}
    return {
        "region": config.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
        "log_group": config.get("log_group") or os.environ.get("CW_LOG_GROUP"),
        "log_stream": config.get("log_stream") or os.environ.get("CW_LOG_STREAM"),
    }


def logs_client(config=None):
    cfg = load_config(config)
    return boto3.client("logs", region_name=cfg["region"])


def cloudwatch_logs_hostname():
    return "logs.amazonaws.com"
