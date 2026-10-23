import os

import boto3


def load_config(config=None):
    config = dict(config or {})
    config.setdefault("region", os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    config.setdefault("log_group", os.getenv("OBSERVABILITY_LOG_GROUP"))
    config.setdefault("log_stream", os.getenv("OBSERVABILITY_LOG_STREAM"))
    return config


def build_logs_client(config=None):
    config = load_config(config)
    return boto3.client("logs", region_name=config.get("region"))
