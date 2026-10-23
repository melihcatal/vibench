import os

import boto3


DEFAULT_MODEL_ID = "amazon.nova-pro-v1:0"


def load_config(config=None):
    config = dict(config or {})
    if "region" not in config:
        config["region"] = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    if "model_id" not in config:
        config["model_id"] = os.environ.get("BEDROCK_MODEL_ID", DEFAULT_MODEL_ID)
    return config


def get_bedrock_client(config=None):
    config = load_config(config)
    return boto3.client("bedrock-runtime", region_name=config.get("region"))


def get_model_id(config=None):
    return load_config(config).get("model_id", DEFAULT_MODEL_ID)
