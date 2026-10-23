import os
import boto3


def get_region(config=None):
    config = config or {}
    return config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")


def get_textract_client(config=None):
    return boto3.client("textract", region_name=get_region(config))


def get_comprehend_client(config=None):
    return boto3.client("comprehend", region_name=get_region(config))


def get_translate_client(config=None):
    return boto3.client("translate", region_name=get_region(config))


def get_bedrock_runtime_client(config=None):
    return boto3.client("bedrock-runtime", region_name=get_region(config))
