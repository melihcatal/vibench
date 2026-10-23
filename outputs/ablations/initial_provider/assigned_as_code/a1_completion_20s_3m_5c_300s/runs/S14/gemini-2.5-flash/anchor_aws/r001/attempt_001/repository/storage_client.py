import boto3
import os


def get_s3_client(region_name=None):
    region = region_name or os.environ.get("AWS_REGION")
    if not region:
        raise ValueError("AWS region must be provided or set in AWS_REGION environment variable.")
    return boto3.client("s3", region_name=region)


def get_textract_client(region_name=None):
    region = region_name or os.environ.get("AWS_REGION")
    if not region:
        raise ValueError("AWS region must be provided or set in AWS_REGION environment variable.")
    return boto3.client("textract", region_name=region)


def get_translate_client(region_name=None):
    region = region_name or os.environ.get("AWS_REGION")
    if not region:
        raise ValueError("AWS region must be provided or set in AWS_REGION environment variable.")
    return boto3.client("translate", region_name=region)


def get_comprehend_client(region_name=None):
    region = region_name or os.environ.get("AWS_REGION")
    if not region:
        raise ValueError("AWS region must be provided or set in AWS_REGION environment variable.")
    return boto3.client("comprehend", region_name=region)


def get_bedrock_runtime_client(region_name=None):
    region = region_name or os.environ.get("AWS_REGION")
    if not region:
        raise ValueError("AWS region must be provided or set in AWS_REGION environment variable.")
    return boto3.client("bedrock-runtime", region_name=region)
