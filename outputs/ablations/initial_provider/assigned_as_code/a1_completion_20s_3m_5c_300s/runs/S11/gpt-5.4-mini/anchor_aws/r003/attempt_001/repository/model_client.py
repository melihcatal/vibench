import os

import boto3


def load_platform_config(overrides=None):
    overrides = overrides or {}
    return {
        "region": overrides.get("region", os.getenv("AWS_REGION", "us-east-1")),
        "model_id": overrides.get("model_id", os.getenv("BEDROCK_MODEL_ID", "us.amazon.nova-pro-v1:0")),
    }


def create_platform_client(config=None):
    config = config or load_platform_config()
    return boto3.client("bedrock-runtime", region_name=config["region"])
