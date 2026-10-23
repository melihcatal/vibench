import os


def get_region(config=None):
    config = config or {}
    return config.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"


def get_model_id(config=None):
    config = config or {}
    return config.get("model_id") or "us.amazon.nova-pro-v1:0"
