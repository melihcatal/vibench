import os

import boto3


def load_observability_config(config=None):
    config = config or {}
    region = config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    log_group = config.get("log_group") or os.getenv("CLOUDWATCH_LOG_GROUP")
    log_stream = config.get("log_stream") or os.getenv("CLOUDWATCH_LOG_STREAM")
    if not log_group:
        raise ValueError("log_group is required")
    return {"region": region, "log_group": log_group, "log_stream": log_stream}


def cloudwatch_logs_client(region=None):
    return boto3.client("logs", region_name=region)


def ensure_log_stream(client, log_group, log_stream):
    if not log_stream:
        return None
    try:
        client.create_log_stream(logGroupName=log_group, logStreamName=log_stream)
    except Exception:
        pass
    return log_stream
