import os

import boto3


DEFAULT_REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
DEFAULT_MODEL = os.getenv("BEDROCK_MODEL_ID") or "amazon.nova-pro-v1:0"


def get_config(config=None):
    merged = dict(config or {})
    if not merged.get("region"):
        merged["region"] = DEFAULT_REGION
    if not merged.get("model_id"):
        merged["model_id"] = DEFAULT_MODEL
    return merged


def get_bedrock_client(config=None):
    merged = get_config(config)
    return boto3.client("bedrock-runtime", region_name=merged.get("region"))


def get_model_id(config=None):
    return get_config(config).get("model_id")
