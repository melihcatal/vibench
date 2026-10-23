import os
import boto3


def get_config(config=None):
    data = dict(config or {})
    if "region" not in data:
        data["region"] = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    return data


def textract_client(config=None):
    data = get_config(config)
    return boto3.client("textract", region_name=data.get("region"))


def comprehend_client(config=None):
    data = get_config(config)
    return boto3.client("comprehend", region_name=data.get("region"))


def bedrock_runtime_client(config=None):
    data = get_config(config)
    return boto3.client("bedrock-runtime", region_name=data.get("region"))
