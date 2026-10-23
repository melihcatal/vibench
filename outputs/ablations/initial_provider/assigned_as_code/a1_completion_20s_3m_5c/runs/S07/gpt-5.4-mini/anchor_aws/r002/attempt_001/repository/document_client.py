import os

import boto3


def get_config(config=None):
    config = config or {}
    region = config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    return {"region": region}


def get_textract_client(config=None):
    cfg = get_config(config)
    return boto3.client("textract", region_name=cfg.get("region"))


def get_translate_client(config=None):
    cfg = get_config(config)
    return boto3.client("translate", region_name=cfg.get("region"))


def get_comprehend_client(config=None):
    cfg = get_config(config)
    return boto3.client("comprehend", region_name=cfg.get("region"))

def get_bedrock_runtime_client(config=None):
    cfg = get_config(config)
    return boto3.client("bedrock-runtime", region_name=cfg.get("region"))
