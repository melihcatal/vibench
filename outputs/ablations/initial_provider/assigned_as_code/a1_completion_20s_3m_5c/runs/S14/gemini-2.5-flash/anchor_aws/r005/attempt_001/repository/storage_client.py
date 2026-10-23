import boto3
import os


def get_s3_client(region_name=None):
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("s3", region_name=region_name)

def get_textract_client(region_name=None):
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("textract", region_name=region_name)

def get_translate_client(region_name=None):
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("translate", region_name=region_name)

def get_comprehend_client(region_name=None):
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("comprehend", region_name=region_name)

def get_bedrock_runtime_client(region_name=None):
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("bedrock-runtime", region_name=region_name)
