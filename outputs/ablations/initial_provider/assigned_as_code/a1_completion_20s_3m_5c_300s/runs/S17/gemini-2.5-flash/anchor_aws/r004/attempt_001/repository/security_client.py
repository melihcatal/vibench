import boto3
import os


def get_kms_client(config=None):
    config = config or {}
    region_name = config.get("region", os.environ.get("AWS_REGION"))
    if not region_name:
        raise ValueError("AWS region not provided in config or AWS_REGION environment variable.")
    return boto3.client("kms", region_name=region_name)


def get_comprehend_client(config=None):
    config = config or {}
    region_name = config.get("region", os.environ.get("AWS_REGION"))
    if not region_name:
        raise ValueError("AWS region not provided in config or AWS_REGION environment variable.")
    return boto3.client("comprehend", region_name=region_name)


def get_bedrock_runtime_client(config=None):
    config = config or {}
    region_name = config.get("region", os.environ.get("AWS_REGION"))
    if not region_name:
        raise ValueError("AWS region not provided in config or AWS_REGION environment variable.")
    return boto3.client("bedrock-runtime", region_name=region_name)


def get_translate_client(config=None):
    config = config or {}
    region_name = config.get("region", os.environ.get("AWS_REGION"))
    if not region_name:
        raise ValueError("AWS region not provided in config or AWS_REGION environment variable.")
    return boto3.client("translate", region_name=region_name)


def get_cloudtrail_client(config=None):
    config = config or {}
    region_name = config.get("region", os.environ.get("AWS_REGION"))
    if not region_name:
        raise ValueError("AWS region not provided in config or AWS_REGION environment variable.")
    return boto3.client("cloudtrail", region_name=region_name)
