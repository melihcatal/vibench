import os

import boto3


def load_platform_config(overrides=None):
    overrides = overrides or {}
    return {
        "region": overrides.get("region") or os.environ.get("AWS_REGION", "us-east-1"),
        "model_id": overrides.get("model_id") or os.environ.get("BEDROCK_MODEL_ID", "us.amazon.nova-pro-v1:0"),
    }


def build_bedrock_runtime_client(config=None):
    config = load_platform_config(config)
    return boto3.client("bedrock-runtime", region_name=config["region"])


def build_bedrock_client(config=None):
    config = load_platform_config(config)
    return boto3.client("bedrock", region_name=config["region"])
