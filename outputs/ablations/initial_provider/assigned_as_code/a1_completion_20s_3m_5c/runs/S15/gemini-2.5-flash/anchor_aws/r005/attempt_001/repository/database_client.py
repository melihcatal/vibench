import boto3
import os

def get_dynamodb_client(region_name=None):
    region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("dynamodb", region_name=region_name)

def get_dynamodb_resource(region_name=None):
    region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.resource("dynamodb", region_name=region_name)

def get_s3_client(region_name=None):
    region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("s3", region_name=region_name)

def get_comprehend_client(region_name=None):
    region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("comprehend", region_name=region_name)

def get_translate_client(region_name=None):
    region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("translate", region_name=region_name)
