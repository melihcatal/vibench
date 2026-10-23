import os
import boto3


def get_observability_client():
    config = {
        "region": os.getenv("AWS_REGION"),
        "log_group": os.getenv("LOG_GROUP_NAME"),
        "log_stream": os.getenv("LOG_STREAM_NAME"),
    }
    return boto3.client("logs", region_name=config["region"]), config